import argparse, logging
import sys, os
from pprint import pprint
from datetime import datetime
from glob import glob

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s:\t%(message)s")
    logger = logging.getLogger()

def genome_fasta(s):
    try:
        genome, taxon= map(int, s.split(','))
        return int(taxon), genome
    except:
        raise argparse.ArgumentTypeError("Genomes must be entered as \"Taxon1,<reference-fasta1> Taxon2,<reference-fasta2>\"")

def genome_list(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        out_list = []
        with open(path) as genomes_in:
            for line in genomes_in:
                line = line.strip().split()
                if len(line) != 2: raise TypeError()
                taxon, genome = line
                out_list.append((taxon, genome))
        return out_list
    except:
        raise argparse.ArgumentTypeError('Must be a path to a tab-seperated file that contains the Taxon in the first '
                                  'column, and the path to the corresponding genome fasta in the second column')

if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    subparsers = parser.add_subparsers(help="The argument specifying the type of analysis: single, "
                                            "or merged")

    parser_single = subparsers.add_parser('single', help='Run ISPeaks on a single fastq file.')
    parser_single.set_defaults(which="single")
    parser_merged = subparsers.add_parser('merged', help='Run ISPeaks on multiple fastq files, merging them to make '
                                                      'the peak calls.')
    parser_merged.set_defaults(which="merged")

    parser_single.add_argument('-fq', '--fastqs', required=True, nargs = 2,
                        help='Two fastq files containing the forward and reverse strands, in that order.')

    parser_single.add_argument('-c', '--classifications', required=True, nargs=2,
                        help='Two tab-separated files where the first column is the read title and the second'
                             'column is the assigned taxon id. The first classification file corresponds to the'
                             'forward reads, and the second file corresponds to the reverse reads, in the same order'
                             'with no reads excluded.')

    parser_single.add_argument('-o', '--output-folder', required=True,
                        help='Specify the output folder to create. If already created, it must be empty.')

    parser_single.add_argument('-is', '--insertion-fasta', required=True, type=str,
                        default=os.path.join(data_dir, "IS_fastas/Bacteroides_all.fasta"),
                        help='A fasta file containing the insertion sequences of interest,'
                             ' concatenated sequentially in any order.')

    genomes_in = parser_single.add_mutually_exclusive_group(required=True)
    genomes_in.add_argument('-gf', '--reference-genome-fastas',
                             type=genome_fasta, nargs='*',
                             help='All the reference genomes to analyze in fasta format. Input must be '
                                'in the format \"<reference-fasta1>,Taxon1 <reference-fasta2>,Taxon2\"')
    genomes_in.add_argument('-gl', '--reference-genome-list',
                             type=genome_list, nargs=1,
                             help='A path to a tab-seperated file that contains the Taxon in the first '
                                  'column, and the path to the corresponding genome fasta in the second column.')

    parser_single.add_argument('-nodes', '--taxon-nodes', required=False, type=list,
                               default=[
                                   os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp")),
                                   os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/merged.dmp"))],
                               help='Location of the NCBI Taxonomy Database nodes.dmp and merged.dmp files',
                               nargs='*')

    parser_single.add_argument('-p', '--threads', required=False,
                        default=1, type = int,
                        help='The number of threads to run with bowtie2 alignments.')

    args = parser.parse_args()
    args = vars(args)

    pprint(args)