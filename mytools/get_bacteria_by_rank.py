import sys, os
import argparse

def main(args):
    print "Getting Nodes and Ranks..."
    nodes, ranks = get_nodes_ranks(args['nodes'])
    print "Number of nodes: %d" % len(nodes)
    print "Number of ranks: %d" % len(ranks)
    print "Getting Names..."
    names = get_names(args['names'])
    print "Number of names: %d" % len(names)

    for line in get_relevant_taxa(args['rank'], ranks, nodes, names):
        print '\t'.join(line)

def get_relevant_taxa(rank, ranks, nodes, names):
    relevant_taxa = {}

    for taxon in names.keys():
        if ranks[taxon] == rank:
            print ranks[taxon], rank
            if is_bacteria(taxon, nodes):
                yield [taxon, rank, names[taxon]]


def get_nodes_ranks(nodes_location):
    taxon_nodes_dict = {}
    ranks_dict = {}
    with open(nodes_location) as nodes_in:
        for line in nodes_in:
            line = line.strip().split("|")
            id = line[0].strip()
            parent_id = line[1].strip()
            rank = line[2]
            taxon_nodes_dict[id] = parent_id
            ranks_dict[id] = rank

    return taxon_nodes_dict, ranks_dict



def get_names(taxon_names_location):

    taxa_to_names = {}

    with open(taxon_names_location) as names_in:
        for line in names_in:
            line = [field.strip() for field in line.strip().split("|")]
            #print "\t".join([line[0], line[1], line[3]])
            if line[3] == 'scientific name':
                taxa_to_names[line[0]] = line[1]

    return taxa_to_names

def is_bacteria(taxon, nodes):
    hierarchy = [taxon]

    while taxon_id != '1' and taxon_id != '0':
        taxon_id = taxon_nodes_dict[taxon_id]
        hierarchy.append(taxon_id)
        if taxon_id == '2':
            return True

    return False



if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "iscounter/data")

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('rank',
                        help='The rank of interest to be extracted.')

    parser.add_argument('--nodes', required=False, type=str,
                        default=os.path.join(data_dir, "TaxonomyDatabase/nodes.dmp"),
                        help='Location of the NCBI Taxonomy Database nodes.txt file')

    parser.add_argument('--names', required=False, type=str,
                        default= os.path.join(data_dir, "TaxonomyDatabase/names.dmp"),
                        help='Location of the NCBI Taxonomy Database names.txt file')

    args = parser.parse_args()
    args = vars(args)

    main(args)


