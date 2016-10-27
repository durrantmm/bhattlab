import argparse, logging
import sys, os
import pprint
from datetime import datetime
from phylophilter import filters

def main(args):

    if not os.path.isdir(args['output_folder']):
        os.mkdir(args['output_folder'])

    write_run_info(args, args['output_folder'])
    read_filter = filters.Filter(args['fastq_reads'], args['read_to_taxid'],args['taxon_nodes'])

    filtered_reads = read_filter.filter_reads_linear(args['taxon_id'], paired_end=args['paired_end'])

    with open(os.path.join(args['output_folder'], ), 'w') as out:
        out.writelines(filtered_reads)

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
                        default=os.path.join(data_dir, "insertion_sequences")
                            ,
                        help='Location of the NCBI Taxonomy Database nodes.txt file')

    parser.add_argument('-o', '--output_folder', required=False,
                        default = os.path.join(output_dir,"ISMapper_%s" % timestamp),
                        help='Specify the output file')

    args = parser.parse_args()
    args = vars(args)

    main(args)

