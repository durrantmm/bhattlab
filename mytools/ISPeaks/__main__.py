import argparse, logging
import sys, os
from pprint import pprint
from datetime import datetime
from glob import glob

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s:\t%(message)s")
    logger = logging.getLogger()

    print args['which']

def genome_fasta(s):
    try:
        print s
        genome, taxon= s.split(',')
        if not os.path.isfile(genome): raise TypeError("Genome fasta is not a file.")
        return int(taxon), genome
    except:
        raise argparse.ArgumentTypeError("Genomes must be entered as \"<reference-fasta1>,Taxon1 "
                                         "<reference-fasta2>,Taxon2...\"")

def genome_list(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        out_list = []
        with open(path) as genomes_in:
            for line in genomes_in:
                line = line.strip().split()
                if len(line) != 2: raise TypeError()
                genome, taxon = line
                out_list.append((int(taxon), genome))
        return out_list
    except:
        raise argparse.ArgumentTypeError('Must be a path to a tab-seperated file that contains'
                                         'the path to the genome fasta in the first and the corresponding'
                                          'taxon in the second column.')

def insertion_fasta(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return path
    except:
        raise argparse.ArgumentTypeError('Please give a path to a valid fasta file.')


def fastq_file(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return path
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid fastq files.')

def class_file(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return path
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid classification files.')

def output_folder(path):
    try:
        if os.path.isdir(path):
            if len(glob(path+'/*')) > 0:
                raise TypeError()
        return path
    except:
        raise argparse.ArgumentTypeError('Output folder must be empty or non-existent.')

def taxon_nodes(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return path
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid taxonomy node files.')


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

    parser_single.add_argument('-fq', '--fastqs', required=True, nargs = 2, type=fastq_file,
                        help='Two fastq files containing the forward and reverse strands, in that order.')

    parser_single.add_argument('-c', '--classifications', required=True, nargs=2, type=class_file,
                        help='Two tab-separated files where the first column is the read title and the second'
                             'column is the assigned taxon id. The first classification file corresponds to the'
                             'forward reads, and the second file corresponds to the reverse reads, in the same order'
                             'with no reads excluded.')

    parser_single.add_argument('-o', '--output-folder', required=True, type=output_folder,
                        help='Specify the output folder to create. If already created, it must be empty.')

    parser_single.add_argument('-is', '--insertion-fasta', required=True, type=insertion_fasta,
                        default=os.path.join(data_dir, "IS_fastas/Bacteroides_all.fasta"),
                        help='A fasta file containing the insertion sequences of interest,'
                             ' concatenated sequentially in any order.')

    genomes_in = parser_single.add_mutually_exclusive_group(required=True)
    genomes_in.add_argument('-gf', '--reference-genome-fastas',
                             type=genome_fasta, nargs='*',
                             help='All the reference genomes to analyze in fasta format. Input must be '
                                'in the format \"<reference-fasta1>,Taxon1 <reference-fasta2>,Taxon2...\"')
    genomes_in.add_argument('-gl', '--reference-genome-list',
                             type=genome_list, nargs=1,
                             help='A path to a tab-seperated file that contains the Taxon in the first '
                                  'column, and the path to the corresponding genome fasta in the second column.')

    parser_single.add_argument('-nodes', '--taxon-nodes', required=False, type=taxon_nodes,
                               default=[taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"))),
                                   taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/merged.dmp")))],
                               help='Location of the NCBI Taxonomy Database nodes.dmp and/or merged.dmp files',
                               nargs='*')

    parser_single.add_argument('-p', '--threads', required=False,
                        default=1, type = int,
                        help='The number of threads to run with bowtie2 alignments.')

    args = parser.parse_args()
    args = vars(args)

    main(args)