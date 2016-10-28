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

    if not os.path.isdir(args['output_folder']):
        os.mkdir(args['output_folder'])

    filtered_fastq_file = os.path.join(args['output_folder'], "filtered_reads.fq")

    logger.info("Saving run info to output folder...")
    write_run_info(args, args['output_folder'])
    read_filter = filters.Filter(args['fastq_reads'], args['read_to_taxid'],args['taxon_nodes'])

    filtered_reads = read_filter.filter_reads_linear_ismapper(args['taxon_id'], paired_end=True)

    logger.info("Filtering reads and saving to output folder...")
    with open(filtered_fastq_file, 'w') as out:
        out.writelines(filtered_reads)
    logger.info("Reads saved to %s" % filtered_fastq_file)

    logger.info("Building all the insertion sequence in the given directory using bowtie2...")
    bowtie2.build_all(args['insertion_sequences'])

    logger.info("Aligning the reads to all the insertion sequences...")
    bowtie2.align_all(args['insertion_sequences'], filtered_fastq_file, args['output_folder'])

    logger.info("Saving summary statistics to results.txt in output directory...")
    save_summary_stats(filtered_fastq_file, args['output_folder'])

    logger.info("Analysis Complete  :)")

def save_summary_stats(filtered_fastq_file, output_dir):
    results_output = os.path.join(output_dir, "results.txt")
    initial_read_count = get_fastq_read_count(filtered_fastq_file)
    print initial_read_count
    sam_files = glob(os.path.join(output_dir, "*.sam"))
    print sam_files

    results = []
    for sam in sam_files:
        sam_aligned_reads = get_sam_read_count(sam)
        results.append([sam.split('.')[0], str(sam_aligned_reads), str(float(sam_aligned_reads) / initial_read_count),
                        str(initial_read_count)])

    with open(results_output,'w') as out:
        header = ['InsertionSequence', '#AlignedReads', '%AlignedReads', 'InitialReadCount']
        print "\t".join(header)
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

    parser.add_argument('-b', '--read_to_taxid', required=True,
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-t', '--taxon_id', required=True,
                        help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-nodes', '--taxon_nodes', required=False, type=list,
                        default=[
                            os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"),
                            os.path.join(data_dir, "TaxonomyDatabase/merged.dmp")],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('-is', '--insertion_sequences', required=False, type=str,
                        default=os.path.join(data_dir, "insertion_sequences"),
                        help='A directory containing the insertion sequences of interest, one file for')

    parser.add_argument('-o', '--output_folder', required=False,
                        default = os.path.join(output_dir,"ISMapper_%s" % timestamp),
                        help='Specify the output file')

    args = parser.parse_args()
    args = vars(args)

    main(args)

