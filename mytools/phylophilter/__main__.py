import sys
import IO
import argparse
import logging
import pprint
import linear, clade, subtree


def main(args):

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.debug(pprint.pformat(args))

    if args['which'] == "linear":
        linear_filter = linear.Filter(args['fastq_reads'], args['read_to_taxid'],
                                      args['taxon_nodes'])

        filtered_reads = linear_filter.filter_reads(args['taxon_id'])

        for read in filtered_reads:
            print read

    elif args['which'] == "clade":
        clade.filter(logger)
    elif args['which'] == "subtree":
        subtree.filter(logger)

    sys.exit()


if __name__ == "__main__":

    # setup the option parser
    top_parser = argparse.ArgumentParser(description='fiter_reads_by_taxon.py is a simple program for filtering the reads '
                                                 'by taxon of interest. Use the -h flag for more information.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    top_parser.add_argument('-fq', '--fastq_reads', required = True,
                        help='The fastq file containing the reads of interest')

    top_parser.add_argument('-c', '--read_to_taxid', required = True,
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    top_parser.add_argument('-t','--taxon_id', required = True,
                            help='The NCBI Taxon ID of the species of interest')

    top_parser.add_argument('-nodes', '--taxon_nodes', required=False,
                        default=[
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    top_parser.add_argument('-ntaxa', '--number_of_parent_taxa', required=False,
                        help='Specify --parent_read_extract if you would like to filter the reads by every read that'
                             'is binned into each node in the hierarchy. Follow this flag with the location of the'
                             'NCBI Taxonomy Database that you would like to use to determine the hierarchy',
                        type=int, default=0)

    top_parser.add_argument('-names', '--use_taxon_names', required=False, help='FILL THIS OUT')


    # Specifying the subparsers
    subparsers = top_parser.add_subparsers(help="The argument specifgying the type of filtering to be performed "
                                   "{linear, clade, subtree}")

    parser_linear = subparsers.add_parser('linear', help="This mode will perform a linear filtering of the results. This technique takes filters out"
                                         "all of the reads at the level of the given taxon_id, and then all reads"
                                         "at each ancestral node up until a specified taxon or depth.")

    parser_clade = subparsers.add_parser('clade', help="This mode will perform a clade-based filtering of the reads. It will filter"
                                        "all of the reads that are assigned to the given taxon-id, or any of its "
                                        "descendents. You can also traverse along the ancestral line to specify a "
                                        "taxon or a depth level of interest.")

    parser_subtree = subparsers.add_parser('subtree', help="This mode performs a combination filter that includes both a linear-based"
                                          "aspect and a clade-based aspect. It filters out the specified clade, and includes"
                                          "the reads allocated to ancestral nodes.")

    # Linear Subparser
    parser_linear.set_defaults(which="linear")
    parser_linear.add_argument('-npe', '--no_paired_ends', required=False,
                               action='store_true', help='Default is for paired ends, set flag for no paired ends.')

    # Clade Subparser
    parser_clade.set_defaults(which="clade")
    parser_clade.add_argument('-npe', '--no_paired_ends', required=False,
                               action='store_true', help='Default is for paired ends, set flag for no paired ends.')

    # Subtree Subparser
    parser_subtree.set_defaults(which="subtree")
    parser_subtree.add_argument('-npe', '--no_paired_ends', required=False,
                               action='store_true', help='Default is for paired ends, set flag for no paired ends.')


    args = top_parser.parse_args()
    args = vars(args)


    main(args)