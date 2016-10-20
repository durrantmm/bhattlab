import argparse
import sys
from collections import defaultdict

# start here when the script is launched


def get_taxon_nodes(nodes_location):
    taxon_nodes_dict = defaultdict(str)
    with open(nodes_location) as nodes_in:
        for line in nodes_in:
            line = line.strip().split("|")
            id = line[0].strip()
            parent_id = line[1].strip()
            taxon_nodes_dict[id] = parent_id
    return taxon_nodes_dict


def get_taxon_hierarchy(taxon_id, taxon_nodes_dict):
    hierarchy = [taxon_id]

    while taxon_id != "1":
        taxon_id = taxon_nodes_dict[taxon_id]
        hierarchy.append(taxon_id)

    return hierarchy


def get_required_reads(reads_to_taxid_location, taxon_id):
    assert type(taxon_id) is list, "taxon_id must be a list"
    assert type(reads_to_taxid_location) is str, "reads_to_taxid_location must be a string specifying file"

    matching_reads = set()
    with open(reads_to_taxid_location) as data_in:
        for line in data_in:
            line = line.strip().split("\t")
            read_title = line[0].strip()
            read_taxon_id = line[1].strip()
            if read_taxon_id in taxon_id:
                matching_reads.add(read_title)

    return matching_reads


def print_hierarchy(taxon_hierarchy):
    assert type(taxon_hierarchy) is list, "the taxon hierarchy must be a list"

    level = 0
    for taxa in taxon_hierarchy[::-1]:
        indent = "".join(["     "]*level)
        print indent+taxa
        level += 1

if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='VariantManager is a software suite that provides '
                                                 'several variant managing services.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_reads',
                        help='The fastq file containing the reads of interest')

    parser.add_argument('read_to_taxid',
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('taxon_nodes',
                        help='Location of the NCBI Taxonomy Database nodes.txt file')

    parser.add_argument('taxon_id', help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-ntaxa', '--number_of_parent_taxa', required=False,
                        help='Specify --parent_read_extract if you would like to filter the reads by every read that'
                             'is binned into each node in the hierarchy. Follow this flag with the location of the'
                             'NCBI Taxonomy Database that you would like to use to determine the hierarchy',
                        type=int, default=0)

    args = parser.parse_args()
    args = vars(args)

    fastq_reads = args['fastq_reads']
    read_to_taxid = args['read_to_taxid']
    taxon_id = args['taxon_id']
    taxon_nodes = args['taxon_nodes']
    ntaxa= args['number_of_parent_taxa']

    print("Loading the Taxonomy Database...")
    taxon_nodes_dict = get_taxon_nodes(taxon_nodes)

    print("Getting Taxon Hierarchy...")
    taxon_hierarchy = get_taxon_hierarchy(taxon_id, taxon_nodes_dict)

    print("Here is the taxon id hierarchy:")
    print_hierarchy(taxon_hierarchy)
    taxon_hierarchy = taxon_hierarchy[0:ntaxa+1]

    print("Collecting reads binned to the following taxa:")
    print_hierarchy(taxon_hierarchy)
    selected_reads = get_required_reads(read_to_taxid, taxon_hierarchy)
    print("Total Reads Collected: %d" % len(selected_reads))



