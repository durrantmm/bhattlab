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
    output_folder = args['output_folder'] + '_' + os.path.basename(args['fastq_reads']).split(".")[0]

    if not os.path.isdir(output_folder): os.mkdir(output_folder)

    logger.info("Saving run info to output folder...")
    write_run_info(args, output_folder)


    logger.info("Building the insertion sequence indices...")
    bowtie2.build('2.2.9', args['insertion_sequence_fasta'])


    logger.info("Aligning the fastq file to the insertion sequences...")
    sam_file_loc = bowtie2.align('2.2.9', args['insertion_sequence_fasta'], args['fastq_reads'], output_folder, threads=args['threads'])


    read_filter = filters.Filter(args['fastq_reads'], args['classification_file'], args['taxon_nodes'], logger_in=logger)

    logger.info("Invoking the Jansen Protocol...")
    taxon_total_count, taxon_IS_count, potential_transfers, intra_IS = read_filter.filter_reads_ISCounter2(sam_file_loc)

    for taxon in taxon_total_count.keys():
        try:
            for IS in taxon_IS_count[taxon]:
                print "\t".join([str(taxon), str(IS), str(taxon_total_count[taxon]),
                                 str(taxon_IS_count[taxon][IS])])
        except KeyError:
            print "\t".join([str(taxon), "NO_MATCHING_INSERTION_SEQUENCES",
                             str(taxon_total_count[taxon]), "NA"])

    logger.info("Analysis Complete  :)")

def save_summary_stats(fastq_orig_name, filtered_fastq_file, output_dir, taxon_filter):
    results_output = os.path.join(output_dir, "results.txt")
    initial_read_count = get_fastq_read_count(filtered_fastq_file)
    sam_files = glob(os.path.join(output_dir, "*.sam"))

    out_header = ['FASTQFile', 'TaxonFilter', 'InitialReadCount',
              'InsertionSequence', 'NumAlignedReads', 'PercAlignedReads']

    results = []
    for sam in sam_files:
        sam_aligned_reads = get_sam_read_count(sam)
        results.append([os.path.basename(fastq_orig_name), taxon_filter, str(initial_read_count),
                        os.path.basename(sam).split('.')[0], str(sam_aligned_reads),
                        str((float(sam_aligned_reads) / initial_read_count)*100)])

    with open(results_output,'w') as out:

        out.write("\t".join(out_header)+"\n")
        for line in results:
            out.write("\t".join(line)+"\n")


def get_fastq_read_count(fastq_file, lines_per_read=4):
    line_count = 0
    with open(fastq_file) as infile:
        for line in infile:
            line_count += 1
    return line_count / lines_per_read

def get_sam_read_count(sam_file):
    line_count = 0
    with open(sam_file) as infile:
        for line in infile:
            if line[0] != '@':
                line_count += 1
    return line_count

def write_run_info(args, output_folder):

    with open(os.path.join(output_folder, "run_info.txt"), 'w') as out:
        out.write(pprint.pformat(args))

if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    output_dir = os.path.join(current_dir, "output")
    timestamp = ":".join([str(datetime.now().time()), str(datetime.now().date())])

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-fq', '--fastq_reads', required=True,
                        help='This is a fastq file containing PAIRED END reads that are in an interleaved format.')

    parser.add_argument('-c', '--classification_file', required=True,
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-nodes', '--taxon_nodes', required=False, type=list,
                        default=[
                            os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"),
                            os.path.join(data_dir, "TaxonomyDatabase/merged.dmp")],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('-is', '--insertion_sequence_fasta', required=False, type=str,
                        default=os.path.join(data_dir, "IS_fastas/Bacteroides_all.fasta"),
                        help='A fasta file containing the insertion sequences of interest,'
                             ' concatenated sequentially in any order.')

    parser.add_argument('-o', '--output_folder', required=False,
                        default = os.path.join(output_dir,"ISMapper_%s" % timestamp),
                        help='Specify the output file')

    parser.add_argument('-p', '--threads', required=False,
                        default=1, type = int,
                        help='The number of threads to run with bowtie2.')

    args = parser.parse_args()
    args = vars(args)

    main(args)

