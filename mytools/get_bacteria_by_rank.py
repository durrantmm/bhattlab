import sys, os
import argparse

def main(args):
    nodes = get_taxon_nodes(args['nodes'])

    relevant_taxa = get_relevant_taxa(args['rank'], args['names'], nodes)


def get_taxon_nodes(nodes_location):
    taxon_nodes_dict = {}
    with open(nodes_location) as nodes_in:
        for line in nodes_in:
            line = line.strip().split("|")
            id = line[0].strip()
            parent_id = line[1].strip()
            taxon_nodes_dict[id] = parent_id
    return taxon_nodes_dict

def get_relevant_taxa(rank, names, nodes):
    relevant_taxa = {}

    with open(names, 'r') as names_in:

        for line in names_in:
            line = line = [field.strip() for field in line.strip().split("|")]
            print line

    return 0



def is_bacteria(taxon, nodes):
    pass



if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('rank',
                        help='The rank of interest to be extracted.')

    parser.add_argument('--nodes', required=False, type=str,
                        default=os.path.join(data_dir, "iscounter/TaxonomyDatabase/nodes.dmp"),
                        help='Location of the NCBI Taxonomy Database nodes.txt file')

    parser.add_argument('--names', required=False, type=str,
                        default= os.path.join(data_dir, "iscounter/TaxonomyDatabase/names.dmp"),
                        help='Location of the NCBI Taxonomy Database names.txt file')

    args = parser.parse_args()
    args = vars(args)

    main(args)


