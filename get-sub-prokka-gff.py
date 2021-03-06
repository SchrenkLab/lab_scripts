#! /usr/bin/env python

"""
given a .gff file from prokka and a set of fasta files containing contigs represented in the gff file, divide the gff file into separate gff files, one for each of the provided contig fasta files to be used to extract separate gff files for ESOM bins that are subsets of a larger assembly must be run from directory containing fasta files.

usage:
python get-sub-prokka-gff.py assembly.gff fasta

Copyright:

    get-sub-prokka-gff  divides a gff file into separate gff files, one for each of the provided contig fasta files

    Copyright (C) 2016  William Brazelton

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# define input files
import sys
gff_file = sys.argv[1]
extension = '*' + sys.argv[2]

# check that files are in proper order in command line
if gff_file[-4:] == '.gff': pass
else:
	print 'Please enter files in this order: assembly.gff extension-of-fasta-files-with-contigs'
	sys.exit()


# create dictionary of fasta filename = contig names in that fasta file
c = {}
l = {}
import glob
for filename in glob.glob(extension):
	with open(filename) as contigs:
		count = 0
		for line in contigs: 
			if line[0] == '>': 
				count = count + 1
				header = line.strip('>')
				header = header.replace('-','_')
				header = header.replace(' ','_')
				header = header.split('_')
				contig_id = header[0] + '_' + header[1]
				if filename in c: c[filename].append(contig_id)
				else: c[filename] = list(tuple([contig_id]))
		l[filename] = count

# write each component of the gff file to the appropriate file			
for filename in c:
	newfilename = filename.replace(sys.argv[2],'gff')
	with open(newfilename,'w') as newfile:
		newfile.write('##gff-version 3\n')
		with open(gff_file) as gff:
			scount = 0
			gcount = 0
			for line in gff:
				if '##sequence-region' in line: 
					cols = line.split(' ')
					contig_name = cols[1]
					contig_name = contig_name.replace('-','_')
					contig_name = contig_name.replace(' ','_')
					contig_name = contig_name.split('_')
					contig_name = contig_name[0] + '_' + contig_name[1]
					if contig_name in c[filename]: 
						newfile.write(line)
						scount = scount + 1
				elif 'ID=PROKKA' in line:
					contig_id = line.split('\t')
					contig_id = contig_id[0].replace('-','_')
					contig_id = contig_id.split('_')
					contig_id = contig_id[0] + '_' + contig_id[1]
					if contig_id in c[filename]: 
						newfile.write(line)
						gcount = gcount + 1
				elif '##FASTA' in line: break		# no need to include FASTA sequences in this gff file - not needed by humann2
	numfasta = l[filename]
	print str(numfasta) + ' FASTA entries in ' + filename
	print str(scount) + ' sequence region lines written to ' + newfilename
	print str(gcount) + ' gff3 format lines written to ' + newfilename
