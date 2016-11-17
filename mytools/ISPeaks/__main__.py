import argparse, logging
import sys, os
from pprint import pprint, pformat
from datetime import datetime
from glob import glob
import bowtie2

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:\t%(message)s")
    logger = logging.getLogger()
    logger.info("Here are the arguments as they given:\n\n%s\n" % pformat(args))

    logger.info("Creating the output directory...")
    try: os.makedirs(args['output_dir'])
    except: pass

    if args['which'] == 'single':
        logger.info("Executing the ISPeaks SINGLE protocol...")
        exec_single(args, logger)

    elif args['which'] == 'merged':
        logger.error("Merged is not yet implemented.")
        sys.exit()

    else:
        logger.error("Something weird just happened...")

def exec_single(args, logger):
    logger.info("Aligning the FASTQ files to the insertion sequences...")
    fastq1_path, fastq2_path = args['fastqs'][0], args['fastqs'][1]
    insertion_path = args['insertion_fasta']
    outdir = args['output_dir']
    threads = args['threads']

    logger.info("Building the insertion fasta file for alignment...")
    bowtie2.build('2.2.9', insertion_path, logger)

    logger.info("Aligning the forward reads in %s to the file %s" % (fastq1_path, insertion_path))
    outsam_fq1 = bowtie2.align_fastq_to_insertions('2.2.9', insertion_path, fastq1_path, outdir,
                                                   'fastq1_to_IS.sam', threads)
    logger.info("Output saved to %s" % outsam_fq1)

    logger.info("Aligning the reverse reads in %s to the file %s" % (fastq2_path, insertion_path))
    outsam_fq2 = bowtie2.align_fastq_to_insertions('2.2.9', insertion_path, fastq2_path, outdir,
                                                   'fastq2_to_IS.sam', threads)
    logger.info("Output saved to %s" % outsam_fq2)

    logger.info("Beginning alignment to all specified reference files...")
    if args['reference_genome_fastas']: refs = args['reference_genome_fastas']
    else: refs = args['reference_genome_list']
    ref_sams = align_to_references(fastq1_path, fastq2_path, refs, outdir, logger)
    print ref_sams


def align_to_references(fastq1, fastq2, references, outdir, logger=None):
    ref_sams = {}
    for ref in references:
        taxon, refpath = ref
        if logger: logger.info("Building the genome fasta file for the file %s..." % refpath)
        bowtie2.build('2.2.9', refpath, logger)

        if logger: logger.info("Aligning the forward reads in %s to the genome found at %s which "
                               "represents the taxon %d" %(fastq1, refpath, taxon))
        outsam = bowtie2.align_to_genome('2.2.9', refpath, fastq1, outdir, 'fastq1_to_%d_genome.sam')
        ref_sams[taxon] = outsam
    return ref_sams

def exec_merged(args, logger):
    pass

def genome_fasta(s):
    try:
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
        ##### TEMPORARY TO MAKE THINGS FASTER, DELETE THIS NEXT LINE LATER #####
        return path
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

    # SINGLE arguments
    parser_single.add_argument('-fq', '--fastqs', required=True, nargs = 2, type=fastq_file,
                        help='Two fastq files containing the forward and reverse strands, in that order.')

    parser_single.add_argument('-c', '--classifications', required=True, nargs=2, type=class_file,
                        help='Two tab-separated files where the first column is the read title and the second'
                             'column is the assigned taxon id. The first classification file corresponds to the'
                             'forward reads, and the second file corresponds to the reverse reads, in the same order'
                             'with no reads excluded.')

    parser_single.add_argument('-o', '--output-dir', required=True, type=output_folder,
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

    # MERGED arguments
    parser_merged.add_argument('-o', '--output-dir', required=True, type=output_folder,
                               help='Specify the output folder to create. If already created, it must be empty.')

    args = parser.parse_args()
    args = vars(args)

    main(args)