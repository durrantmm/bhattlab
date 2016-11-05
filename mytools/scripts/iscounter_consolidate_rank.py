import argparse
from collections import defaultdict

def main(args):

    header = ''
    results_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(tuple)))
    with open(args['results']) as infile:
        header = infile.readline().strip().split()
        for line in infile:
            line = {header[i]:line.strip().split()[i] for i in range(len(header))}
            results_dict[line['Date']][line['Taxon']][line['InsertionSequence']] = (line['InitialReadCount'], line['NumAlignedReads'])

    for date in results_dict:
        print date
        for taxon in results_dict[date]:
            print taxon
            for IS in results_dict[date][taxon]:
                print IS
                for final in results_dict[dict][date][taxon]:
                    print final,
                print

if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('results', help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)

    main(args)