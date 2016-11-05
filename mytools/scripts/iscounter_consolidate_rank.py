import argparse
from collections import defaultdict

def main(args):

    header = ''
    results_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(tuple)))
    with open(args['results']) as infile:
        header = infile.readline()
        for line in infile:
            print line



if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('results', help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)

    main(args)