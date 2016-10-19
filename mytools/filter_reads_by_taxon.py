import argparse

# start here when the script is launched

def get_taxon_nodes(nodes_location):
    with open(nodes_location) as nodes_in:
        for line in nodes_in:
            line = line.strip()
            print line
    return "PASS"

def get_taxon_hierarchy(taxon_id):
    pass

if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='VariantManager is a software suite that provides '
                                                 'several variant managing services.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('taxon_nodes', help='This is an updated version of the NCBI Taxonomy Database "nodes.txt" file.')
    parser.add_argument('taxon_id',
                        help='The NCBI Taxon ID of the species of interest')
    #parser.add_argument('fastq_reads', help='The name of the project being used.')
    #parser.add_argument('assigned_read_taxa', help='The name of the project being used.')

    args = parser.parse_args()
    args = vars(args)

    taxon_nodes dict = get_taxon_nodes(taxon_nodes)


