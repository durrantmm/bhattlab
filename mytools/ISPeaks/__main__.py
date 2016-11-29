import argparse
import os
import sys
from pprint import pformat

import call.state

from call import argparseTypes, executive


def main(args):

    if args['which'] == 'call':

        mystate = call.state.CallState(args)
        logger = mystate.logger

        logger.info("Here are the arguments as they were given:\n\n%s\n" % pformat(args))

        logger.info("Executing the ISPeaks SINGLE protocol...")

        executive.action(mystate)

    elif args['which'] == 'merge':
        pass

    else:
        pass
        #logger.error("Something weird just happened...")



if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    subparsers = parser.add_subparsers(help="The argument specifying the type of analysis: single, "
                                            "or merged")

    parser_call = subparsers.add_parser('call', help='Run ISPeaks on a single fastq file to call al lthe peaks')
    parser_call.set_defaults(which="call")
    parser_merge = subparsers.add_parser('merge', help='Run ISPeaks on multiple ISPeaks output folders.')
    parser_merge.set_defaults(which="merge")

    # SINGLE arguments
    parser_call.add_argument('-fq', '--fastqs', required=True, nargs = 2, type=argparseTypes.fastq_file,
                               help='Two fastq files containing the forward and reverse strands, in that order.')

    parser_call.add_argument('-c', '--classifications', required=True, nargs=2, type=argparseTypes.class_file,
                               help='Two tab-separated files where the first column is the read title and the second'
                             'column is the assigned taxon id. The first classification file corresponds to the'
                             'forward reads, and the second file corresponds to the reverse reads, in the same order'
                             'with no reads excluded. MUST HAVE A HEADER.')

    parser_call.add_argument('-cce', '--complete-class-exclusions', required=False, nargs='*',
                               type=argparseTypes.complete_class_exclude,
                               help='A filter used to exclude certain reads if either class column matches the value. '
                                    'Input as \"<Column Name1>=<Criterion1> <Column Name2>=<Criterion2>...\"')

    parser_call.add_argument('-gce', '--genome-class-exclusions', required=False, nargs='*',
                               type=argparseTypes.genome_class_exclude,
                               default=[argparseTypes.genome_class_exclude("PASSEDFILTER=F"),
                                        argparseTypes.genome_class_exclude("TAXID=0")],
                               help='A filter used to exclude certain reads if the genome-aligned read has a column '
                                    'that matches the given value. '
                                    'Input as \"<Column Name1>=<Criterion1> <Column Name2>=<Criterion2>...\"')

    parser_call.add_argument('-ice', '--insertion-class-exclusions', required=False, nargs='*',
                               type=argparseTypes.IS_class_exclude,
                               help='A filter used to exclude certain reads if the IS-aligned read has a column '
                                    'that matches the given value. '
                                    'Input as \"<Column Name1>=<Criterion1> <Column Name2>=<Criterion2>...\"')

    parser_call.add_argument('-o', '--output-dir', required=True, type=argparseTypes.output_folder,
                               help='Specify the output folder to create. If already created, it must be empty.')

    parser_call.add_argument('-is', '--insertion-fasta', required=True, type=argparseTypes.insertion_fasta,
                               default=os.path.join(data_dir, "IS_fastas/Bacteroides_all.fasta"),
                               help='A fasta file containing the insertion sequences of interest,'
                             ' concatenated sequentially in any order.')

    parser_call.add_argument('-g', '--reference-genomes', nargs='+',
                               type=argparseTypes.genome, required = True,
                               help='Reference genomes to analyze in fasta format. Input must be '
                                'in the format \"<reference-fasta1> <reference-fasta2>\"')

    parser_call.add_argument('-nodes', '--taxon-nodes', required=False, type=argparseTypes.taxon_nodes,
                               default=[argparseTypes.taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"))),
                                        argparseTypes.taxon_nodes(os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/merged.dmp")))],
                               help='Location of the NCBI Taxonomy Database nodes.dmp and/or merged.dmp files',
                               nargs='+')

    parser_call.add_argument('-names', '--taxon-names', required=False, type=argparseTypes.taxon_names,
                               default=argparseTypes.taxon_nodes(
                                   os.path.abspath(os.path.join(data_dir, "TaxonomyDatabase/names.dmp"))),
                               help='Location of the NCBI Taxonomy Database names.dmp')

    parser_call.add_argument('-n', '--num_reads', required=False, type=int,
                               help='The total number of paired-end reads. If not given, it will be calculated by counting'
                                    'the number of lines in one of the given classification files')

    parser_call.add_argument('-p', '--threads', required=False,
                        default=1, type = int,
                        help='The number of threads to run with bowtie2 alignments. This is typically (number'
                             ' of available processors) / 2.')

    # MERGED arguments
    parser_merge.add_argument('-d', '--ispeaks_directories', required=True,
                              nargs='+',
                              type=argparseTypes.output_folder,
                              help='Include 2 or more ISPeaks output directories to merge')

    parser_merge.add_argument('-o', '--output-dir', required=True, type=argparseTypes.output_folder,
                               help='Specify the output folder to create. If already created, it must be empty.')

    args = parser.parse_args()
    args = vars(args)

    main(args)