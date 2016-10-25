import sys
import IO
import argparse
import logging
import pprint
import Filters, clade, subtree


def main(args):

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.debug(pprint.pformat(args))

    if args['which'] == "linear":
        myfilter = Filters.Filter(args['fastq_reads'], args['read_to_taxid'],
                                       args['taxon_nodes'], logger)

        filtered_reads = myfilter.filter_reads_linear(args['taxon_id'], args['paired_end'])

        sys.exit()
        for reads, classifs in filtered_reads:
            print reads
            print classifs
            print

    elif args['which'] == "clade":
        clade.filter(logger)
    elif args['which'] == "subtree":
        subtree.filter(logger)

    sys.exit()


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='fiter_reads_by_taxon.py is a simple program for filtering the reads '
                                                 'by taxon of interest. Use the -h flag for more information.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-fq', '--fastq_reads', required = True,
                        help='The fastq file containing the reads of interest')

    parser.add_argument('-c', '--read_to_taxid', required = True,
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-t', '--taxon_id', required = True,
                        help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-nodes', '--taxon_nodes', required=False, type=list,
                        default=[
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('-ntaxa', '--number_of_parent_taxa', required=False,
                        help='Specify --parent_read_extract if you would like to filter the reads by every read that'
                             'is binned into each node in the hierarchy. Follow this flag with the location of the'
                             'NCBI Taxonomy Database that you would like to use to determine the hierarchy',
                        type=int, default=0)

    parser.add_argument('-names', '--use_taxon_names', required=False, help='FILL THIS OUT')


    group_modes = parser.add_mutually_exclusive_group()
    group_modes.add_argument('-l','--linear', action = 'store_true', default = False,
                             help="This mode will perform a linear filtering of the results. This technique takes "
                                  "filters out all of the reads at the level of the given taxon_id, and then all reads"
                                  "at each ancestral node up until a specified taxon or depth.")

    group_modes.add_argument('-c', '--clade', action='store_true', default = False,
                             help="This mode will perform a clade-based filtering of the reads. It will filter"
                                  "all of the reads that are assigned to the given taxon-id, or any of its "
                                  "descendents. You can also traverse along the ancestral line to specify a "
                                  "taxon or a depth level of interest.")

    group_modes.add_argument('-s', '--subtree', action='store_true', default = False,
                             help="This mode performs a combination filter that includes both a linear-based"
                                  "aspect and a clade-based aspect. It filters out the specified clade, and includes "
                                  "the reads allocated to ancestral nodes.")

    args = parser.parse_args()
    args = vars(args)


    main(args)