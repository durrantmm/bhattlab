import argparse
import sys
from collections import defaultdict
from Bio import SeqIO

def main(args):
    genome = get_reference(args['genome'])
    genome.seq = genome.seq[int(args['range'][0]): int(args['range'][1])]

    print "> %s %s-%s" % (args['genome'].split('.')[0], args['range'][0], args['range'][1])
    print genome.seq

def get_reference(reference_loc):
    reference = {}
    with open(reference_loc) as refin:
        reference = SeqIO.to_dict(SeqIO.parse(refin, "fasta"))
    ref = reference[reference.keys()[0]]
    return ref



if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('-g', '--genome', required=True, help='FILL THIS OUT')
    parser.add_argument('-r', '--range', required=True, help='FILL THIS OUT', nargs=2)

    args = parser.parse_args()
    args = vars(args)


    main(args)