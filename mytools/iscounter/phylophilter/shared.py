
def get_taxon_nodes(nodes_locations, logger=None):
    assert type(nodes_locations) is list, "The nodes location must be a list of file locations."

    if logger: logger.info("Loading the taxonomy nodes for the analysis.")

    taxon_nodes_dict = {}
    for location in nodes_locations:
        with open(location) as nodes_in:
            for line in nodes_in:
                line = line.strip().split("|")
                id = line[0].strip()
                parent_id = line[1].strip()
                taxon_nodes_dict[id] = parent_id
    return taxon_nodes_dict

def get_taxon_hierarchy_list(taxon_id, taxon_nodes_dict):
    hierarchy = [taxon_id]

    while taxon_id != '1' and taxon_id != '0':
        taxon_id = taxon_nodes_dict[taxon_id]
        hierarchy.append(taxon_id)

    return hierarchy

def get_taxon_hierarchy_set(taxon_id, taxon_nodes_dict):
    hierarchy = set([taxon_id])

    while taxon_id != '1' and taxon_id != '0':
        taxon_id = taxon_nodes_dict[taxon_id]
        hierarchy.add(taxon_id)

    return hierarchy



### USING LISTS FOR BETTER SPEED