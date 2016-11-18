import argparse, logging
import sys, os
from pprint import pprint, pformat

from glob import glob
import bowtie2, argparseTypes, executive, misc
from log import Log

def main(args):
    args['output_dir'] = misc.makedir(args['output_dir'])


    logger = Log(args['output_dir'])
    logger.info("Here are the arguments as they were given:\n\n%s\n" % pformat(args))

    if args['which'] == 'single':
        logger.info("Executing the ISPeaks SINGLE protocol...")
        executive.exec_single(args, logger)
        sys.exit()

    elif args['which'] == 'merged':
        logger.error("The MERGED protocol is not yet implemented.")
        sys.exit()
        executive.exec_merged(args, logger)


    else:
        logger.error("Something weird just happened...")




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

    # SINGLE arguments
    parser_single.add_argument('-fq', '--fastqs', required=True, nargs = 2, type=argparseTypes.fastq_file,
                        help='Two fastq files containing the forward and reverse strands, in that order.')

    parser_single.add_argument('-c', '--classifications', required=True, nargs=2, type=argparseTypes.class_file,
                        help='Two tab-separated files where the first column is the read title and the second'
                             'column is the assigned taxon id. The first classification file corresponds to the'
                             'forward reads, and the second file corresponds to the reverse reads, in the same order'
                             'with no reads excluded. MUST HAVE A HEADER.')

    parser_single.add_argument('-o', '--output-dir', required=True, type=argparseTypes.output_folder,
                        help='Specify the output folder to create. If already created, it must be empty.')

    parser_single.add_argument('-is', '--insertion-fasta', required=True, type=argparseTypes.insertion_fasta,
                        default=os.path.join(data_dir, "IS_fastas/Bacteroides_all.fasta"),
                        help='A fasta file containing the insertion sequences of interest,'
                             ' concatenated sequentially in any order.')

    parser_single.add_argument('-g', '--reference-genomes', nargs='+',
                             type=argparseTypes.genome, required = True,
                             help='Reference genomes to analyze in fasta format. Input must be '
                                'in the format \"<reference-fasta1> <reference-fasta2>\"')

    parser_single.add_argument('-nodes', '--taxon-nodes', required=False, type=argparseTypes.taxon_nodes,
                               default=[argparseTypes.taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"))),
                                        argparseTypes.taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/merged.dmp")))],
                               help='Location of the NCBI Taxonomy Database nodes.dmp and/or merged.dmp files',
                               nargs='+')

    parser_single.add_argument('-p', '--threads', required=False,
                        default=1, type = int,
                        help='The number of threads to run with bowtie2 alignments. This is typically (number'
                             ' of available processors) / 2.')

    # MERGED arguments
    parser_merged.add_argument('-o', '--output-dir', required=True, type=argparseTypes.output_folder,
                               help='Specify the output folder to create. If already created, it must be empty.')

    args = parser.parse_args()
    args = vars(args)

    main(args)