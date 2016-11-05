import argparse
import sys
from collections import defaultdict

def main(args):

    header = ''
    results_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(tuple)))
    with open(args['results']) as infile:
        header = infile.readline().strip().split()
        for line in infile:
            line = {header[i]:line.strip().split()[i] for i in range(len(header))}
            results_dict[line['Date']][line['Taxon']][line['InsertionSequence']] = (line['InitialReadCount'], line['NumAlignedReads'])

    taxon_dict = get_taxon_nodes(args['nodes'])
    print taxon_dict
    sys.exit()
    for date in results_dict:
        sub_taxa = defaultdict(set)
        for taxon in results_dict[date]:
            pass

def get_taxon_nodes(nodes_locations, logger=None):
    assert type(nodes_locations) is list, "The nodes location must be a list of file locations."

    taxon_nodes_dict = {}
    for location in nodes_locations:
        with open(location) as nodes_in:
            for line in nodes_in:
                line = line.strip().split("|")
                id = line[0].strip()
                parent_id = (line[2].strip(), line[1].strip())
                taxon_nodes_dict[id] = parent_id
    return taxon_nodes_dict

if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('results', help='FILL THIS OUT')
    parser.add_argument('--nodes', required=False,
                        default=["/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/iscounter2/data/TaxonomyDatabase/nodes.dmp",
                                "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/iscounter2/data/TaxonomyDatabase/merged.dmp"],
                        help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)

    main(args)