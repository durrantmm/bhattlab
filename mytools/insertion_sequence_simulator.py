import argparse
import sys
from collections import defaultdict
from Bio import SeqIO

# start here when the script is launched

def main(args):
    reference = {}
    with open(args['reference']) as refin:
        reference = SeqIO.to_dict(SeqIO.parse(refin, "fasta"))

    print reference[ reference.keys()[0]].SeqRecord


def get_n_indices(ref_file):
    for line in ref_file:
        if line.startswith(">"):
            print line




if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('-r', '--reference', required=True, help='FILL THIS OUT')
    parser.add_argument('-i', '--insertion', required=True, help='FILL THIS OUT')
    parser.add_argument('-n', '--number', required=False, default=1, help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)


    main(args)
