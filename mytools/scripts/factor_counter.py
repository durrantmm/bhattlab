import sys
from collections import defaultdict
import argparse

def main(args):
    colnum = args['column']
    file_in = args['file']

    factor_counts = defaultdict(int)
    with open(file_in) as infile:
        for line in infile:
            line = line.strip().split()
            factor_counts[line[colnum]] += 1


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('file', type = str)
    parser.add_argument('-c', '--column', required=True, type=int,
                        help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)

    main(args)