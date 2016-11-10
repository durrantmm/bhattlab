import argparse, logging
import sys, os
import pprint
from datetime import datetime
from phylophilter import filters
import bowtie2
from glob import glob

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s:\t%(message)s")
    logger = logging.getLogger()

    run_info = get_run_info(args['iscounter_output_folder'])

def get_run_info(iscounter_out):
    print glob(os.path.join([iscounter_out, "/*"]))


if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    output_dir = os.path.join(current_dir, "output2")
    timestamp = ":".join([str(datetime.now().time()), str(datetime.now().date())])

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-f', '--iscounter_output_folder', required=True,
                        help='This is the output folder of the ISCounter output of interest.')

    parser.add_argument('-is', '--insertion_sequence', required=True,
                        help='The insertion sequence in the results that are to be analyzed')

    parser.add_argument('-t', '--taxon', required=True,
                        help='The taxon of interest to analyze')

    parser.add_argument('-g', '--genome', required=True,
                        help='A genome, or other fasta file of interest, to align the flanks to.')

    args = parser.parse_args()
    args = vars(args)

    main(args)

