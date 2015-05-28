#!/usr/bin/env python

'''uniqueFastaId alters the id of each FASTA entry in a file

Some programs such as IDBA-UD may create multiple fasta/q files where
the ID of the entries in each file are identical. uniqueFastaId simply takes a
fasta/q file and appends a user defined string to each Fasta Header ID to
ensure that each file will not have headers that clash if the files need to be
concatenated for use by various programs.

Usage: uniqueFastaId.py <fasta/q file> <string to append> [options]

    --version, -v prints version and exits
'''

__version__ = '0.10'

import argparse
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from bioinformatic_tools import fastaOrFastq
from bioinformatic_tools import qualityCheck

def appendStringToHeaders(in_file, string_to_append):
    #Appends string to each FASTA Header ID
    fileType = fastaOrFastq(in_file)
    with open(in_file, 'r') as in_handle:
        out_file = ''
        for i in in_file.split('.')[0:-1]:
            out_file += i
        out_file += '.unique.' + fileType
        with open(out_file, 'a') as out_handle:
            for seq_record in SeqIO.parse(in_handle, fileType):
                seq_record.description +=  string_to_append
                seq_record.id = ''
                SeqIO.write(seq_record, out_handle, fileType)
    qualityCheck(out_file, fileType, in_file, out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'appends a string to to all'\
                                     + ' Header IDs in a FASTA/Q file')
    parser.add_argument('input_file',\
                        default = None,\
                        nargs='?',\
                        help = 'FASTA/Q file to modify')
    parser.add_argument('string_to_append',\
                       default = None,\
                        nargs='?',\
                       help = 'the string to add to each ID the file')
    parser.add_argument('--version', '-v',\
                        help = 'prints version and exits',\
                        action = 'store_true')
    args = parser.parse_args()
    
    if args.version:
        print(__version__)
        sys.exit(0)
    elif args.input_file == None and args.string_to_append == None:
        print(__doc__)
        sys.exit(0)
    elif args.input_file == None or args.string_to_append == None:
        print('Must specify an input file and/or string to append.')
        sys.exit(1)
    else:
        appendStringToHeaders(args.input_file, args.string_to_append)