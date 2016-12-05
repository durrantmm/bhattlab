import sys
from collections import defaultdict
import argparse

def main(args):
    colnum = args['column']
    file_in = args['file']
    delimiter = args['delimiter']
    outpath = args['outfile']

    factor_counts = defaultdict(int)
    with open(file_in) as infile:
        for line in infile:
            line = line.strip().split(delimiter)
            factor_counts[line[colnum]] += 1

    header = ['Factor', 'Count']
    if outpath:
        with open(outpath) as file_out:
            file_out.write(delimiter.join(header)+'\n')

            for key in factor_counts:
                file_out.write(delimiter.join([key, str(factor_counts[key])])+'\n')
    else:
        print delimiter.join(header)
        for key in factor_counts:
            print delimiter.join([key, str(factor_counts[key])])


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('file', type = str)
    parser.add_argument('-c', '--column', required=True, type=int,
                        help='FILL THIS OUT')
    parser.add_argument('-d', '--delimiter', required=False, default='\t',
                        help='FILL THIS OUT')
    parser.add_argument('-o', '--outfile', required=False,
                        help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)

    main(args)