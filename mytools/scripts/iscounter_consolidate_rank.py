import argparse
import sys
from collections import defaultdict

def main(args):

    header = ''
    results_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(tuple)))
    all_taxa = set()
    with open(args['results']) as infile:
        header = infile.readline().strip().split()
        for line in infile:
            line = {header[i]:line.strip().split()[i] for i in range(len(header))}
            results_dict[line['Date']][line['Taxon']][line['InsertionSequence']] = (line['InitialReadCount'], line['NumAlignedReads'])
            all_taxa.add(line['Taxon'])

    taxon_dict = get_taxon_nodes(args['nodes'])

    for date in results_dict:
        for taxon in results_dict[date]:
            sub_taxa = defaultdict(set)
            cur_taxon = taxon_dict[taxon][1]
            children = set([taxon])
            while cur_taxon != '1':
                if taxon_dict[cur_taxon][0] == 'species' or taxon_dict[cur_taxon][0] == 'genus':
                    for child in children:
                        sub_taxa[cur_taxon].add(child)
                cur_taxon = taxon_dict[cur_taxon][1]
                children.add(cur_taxon)

            for taxon in sub_taxa:
                sub_taxa[taxon] = sub_taxa[taxon]-set([taxon])


        print sub_taxa
        sys.exit()



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