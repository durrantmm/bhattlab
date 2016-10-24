import sys
import argparse

def main():

    # setup the option parser
    parser = argparse.ArgumentParser(description='fiter_reads_by_taxon.py is a simple program for filtering the reads '
                                                 'by taxon of interest. Use the -h flag for more information.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_reads',
                        help='The fastq file containing the reads of interest')

    parser.add_argument('read_to_taxid',
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-nodes', '--taxon_nodes', required=False,
                        default=[
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('taxon_id', help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-ntaxa', '--number_of_parent_taxa', required=False,
                        help='Specify --parent_read_extract if you would like to filter the reads by every read that'
                             'is binned into each node in the hierarchy. Follow this flag with the location of the'
                             'NCBI Taxonomy Database that you would like to use to determine the hierarchy',
                        type=int, default=0)

    parser.add_argument('-names', '--use_taxon_names', required=False, help='FILL THIS OUT')

    parser.add_argument('-b', '--branched', action='store_true')

    parser.add_argument('-p', '--paired_ends', action='store_true', default=False,
                        help="Account for the assigned taxon for each read in the pair. If one passes the taxon test,"
                             "it is included.")

    args = parser.parse_args()
    args = vars(args)

    print args()
    fastq_reads = args['fastq_reads']
    read_to_taxid = args['read_to_taxid']
    taxon_id = args['taxon_id']
    taxon_nodes = args['taxon_nodes']
    ntaxa = args['number_of_parent_taxa']
    taxon_names = args['use_taxon_names']
    branched = args['branched']
    paired_ends = args['paired_ends']

    if taxon_names == "default":
        taxon_names = "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/names.dmp"

    taxa2names = None

    if taxon_names:
        print("Retrieving taxon names as requested...")
        taxa2names = get_taxa_to_names(taxon_names)

    print("Loading the taxonomy database...")
    taxon_nodes_dict = get_taxon_nodes(taxon_nodes)
    if not is_taxon_id_in_nodes(taxon_id, taxon_nodes_dict):
        print("The given taxon ID is not in the database, it may be deleted from the "
              "official database, or your database is outdated.")
        sys.exit()

    print("Taxon of Interest:")
    print("\t" + taxon_id)
    if taxon_names: print taxon_id_to_name(taxon_id, taxa2names)

    print("Getting taxon hierarchy...")
    taxon_hierarchy = get_taxon_hierarchy(taxon_id, taxon_nodes_dict)

    print("Here is the taxon id hierarchy:")
    print_hierarchy(taxon_hierarchy, taxa2names)
    taxon_hierarchy = taxon_hierarchy[0:ntaxa + 1]

    if not branched:

        if paired_ends:
            print("Collecting reads binned to the following taxa, including PAIRED ENDS:")
            out_file = "reads_filtered_%s_to_%s_ntaxa%d_PAIRED_ENDS_LINEAR.fastq" % \
                       (taxon_hierarchy[0], taxon_hierarchy[-1], ntaxa)
            print("Writing out to file: %s" % out_file)
            selected_reads = get_required_reads_paired_linear(read_to_taxid, fastq_reads, taxon_hierarchy, out_file)

        else:
            print("Collecting reads binned to the following taxa:")
            print_hierarchy(taxon_hierarchy, taxa2names)
            out_file = "reads_filtered_%s_to_%s_ntaxa%d_LINEAR.fastq" % (taxon_hierarchy[0], taxon_hierarchy[-1], ntaxa)
            print("Writing out to file: %s" % out_file)
            selected_reads = get_required_reads_linear(read_to_taxid, fastq_reads, taxon_hierarchy, out_file)

        print("Total Reads Collected: %d" % len(selected_reads))

    else:
        out_file = "reads_filtered_%s_to_%s_ntaxa%d_BRANCHED.fastq" % (taxon_hierarchy[0], taxon_hierarchy[-1], ntaxa)

        print("Collecting reads binned to the following taxa, and ALL CHILDREN TAXA:")
        print_hierarchy(taxon_hierarchy, taxa2names)
        print("Writing out to file: %s" % out_file)
        selected_reads, children_taxa = get_required_reads_branched(read_to_taxid, fastq_reads, taxon_hierarchy,
                                                                    taxon_nodes_dict, out_file)
        print("Total Reads Collected: %d" % len(selected_reads))

        print("Children Taxa Included:")
        col_width_species = max(len(taxon_id_to_name(taxon, taxa2names)) for taxon in children_taxa.keys()) + 2
        col_width_ids = max(
            len(str(max([int(taxon), int(children_taxa[taxon])]))) for taxon in children_taxa.keys()) + 2

        for child in children_taxa:
            print "".join([str(child).ljust(col_width_ids), str(children_taxa[child]).ljust(col_width_ids),
                           taxon_id_to_name(child, taxa2names).replace(" ", "_").ljust(col_width_species)])


if __name__ == "__main__":
    main()