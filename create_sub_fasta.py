#!/usr/bin/env python

"""extracts entries from samples based on IDs and writes them to a new file

Usage:

    create_sub_fasta.py <output> [--ids] [--files] [--coverage] [--fastq]

Synopsis:

    Scans FASTA or FASTQ files for headers that match at least one
    ID. If a header matches an ID, the entire entry is written to
    a new FASTA or FASTQ file.

Required Arguments:

    output:        Name of file to write matches to
    --ids:         One or more IDs to search for
    --files:       One or more FASTA or FASTQ files to search

Optional Arguments:

    --fastq:       Specifies input files as FASTQ files [Default: FASTA]
"""

from __future__ import print_function
import argparse
from bio_utils.iterators.gff3 import gff3_iter
import re
from screed.fasta import fasta_iter
from screed.fastq import fastq_iter
import sys

__author__ = 'Alex Hyer'
__version__ = '0.0.0.4'


def compile_ids(ids):
    """Converts IDs to raw strings, compiles them, and returns them as a list"""

    compiled_ids = []
    for id in ids:
        compiled_ids.append(re.compile(repr(id)))
    return compiled_ids


def fastaq_iter(file_handle, fastq=False):
    """Yields entries from a FASTA or FASTQ file, recreates original header"""    
 
    fastaq_iterator = fasta_iter if not fastq else fastq_iter
    for entry in fastaq_iterator(file_handle):
        if not fastq:
            entry['name'] = '{0} {1}'.format(entry['name'], \
                                             entry['description'])
        else:
            entry['name'] = '{0} {1}'.format(entry['name'], \
                                             entry['annotations'])
        yield entry


def extract_ids(ids, files, fastq=False):
    """Extract entries with multiple IDs from multiple samples"""

    entries = []
    compiled_ids = compile_ids(ids)
    for file in files:
        with open(file, 'rU') as in_handle:
            for entry in fastaq_iter(in_handle, fastq=fastq):
                for compiled_id in compiled_ids:
                    if len(compiled_id.findall(entry['name'])) == 1:
                        to_return = ''
                        if not fastq:
                            to_return = '>{0}\n{1}\n'.format(entry['name'],
                                                             entry['sequence'])
                        else:
                            to_return = '@{0}\n{1}\n+\n{2}\n'.format(
                                                             entry['name'],
                                                             entry['sequence'],
                                                             entry['accuracy'])      
                        # Stop after first ID match
                        break
                        entries.append(to_return)
    return entries
                    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('output',
                        default=None,
                        nargs='?',
                        help='name of FASTA or FASTQ file to write')
    parser.add_argument('--fastq',
                        default=False,
                        action='store_true',
                        help='specify input file as FASTQ file [Default: FASTA]')
    parser.add_argument('--files',
                        default=None,
                        nargs='*',
                        help='Files to extract IDs from')
    parser.add_argument('--ids', metavar='IDs',
                        default=None,
                        nargs='*',
                        help='IDs to extract from input files')
    args = parser.parse_args()

    if args.output is None:
        print(__doc__)
        sys.exit(0)
    elif args.ids is None and args.files is None:
        print('Must specify one or more IDs and one or more files.')
        sys.exit(1)
    else:
        entries = extract_ids(args.ids, args.files, fastq=args.fastq)

    with open(args.output, 'w') as out_handle:
        for entry in entries:
            out_handle.write(entry)
    
    sys.exit(0)
