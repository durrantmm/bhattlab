import argparse
import sys
from collections import defaultdict

# start here when the script is launched


def get_taxon_nodes(nodes_locations):
    taxon_nodes_dict = {}
    for location in nodes_locations:
        with open(location) as nodes_in:
            for line in nodes_in:
                line = line.strip().split("|")
                id = line[0].strip()
                parent_id = line[1].strip()
                taxon_nodes_dict[id] = parent_id
    return taxon_nodes_dict


def get_taxon_hierarchy(taxon_id, taxon_nodes_dict):
    hierarchy = [taxon_id]

    while taxon_id != '1' and taxon_id != '0':
        taxon_id = taxon_nodes_dict[taxon_id]
        hierarchy.append(taxon_id)

    return hierarchy

def is_child_taxon(taxon_id, taxon_nodes_dict, stop_set):
    hierarchy = [taxon_id]

    while taxon_id != '1' and taxon_id != '0':
        if taxon_id in stop_set:
            return True
        else:
            taxon_id = taxon_nodes_dict[taxon_id]
            hierarchy.append(taxon_id)

    return False


def get_required_reads_linear(reads_to_taxid_location, fastq_reads, taxon_id, out_file_loc):
    assert type(taxon_id) is list, "taxon_id must be a list"
    assert type(reads_to_taxid_location) is str, "reads_to_taxid_location must be a string specifying file"

    matching_reads = set()
    with open(reads_to_taxid_location) as read_taxa_in:

        with open(fastq_reads) as fastq_reads_in:

            with open(out_file_loc, 'w') as out_file:
                read_taxa_in.readline()

                for taxa_line in read_taxa_in:
                    fastq_lines = [fastq_reads_in.readline().strip() for i in range(4)]
                    taxa_line = taxa_line.strip().split("\t")
                    read_title = taxa_line[0].strip()
                    read_taxon_id = taxa_line[1].strip()

                    if read_title != fastq_lines[0]:
                        print "ERROR: Please make sure that fastq_reads and read_to_taxid are in the same sorted order"
                        sys.exit()

                    if read_taxon_id in taxon_id:
                        matching_reads.add(read_title)
                        out_file.write("\n".join(fastq_lines)+"\n")

    return matching_reads


def get_required_reads_paired_linear(reads_to_taxid_location, fastq_reads, taxon_hierarchy, out_file_loc):
    assert type(taxon_hierarchy) is list, "taxon_id must be a list"
    assert type(reads_to_taxid_location) is str, "reads_to_taxid_location must be a string specifying file"

    matching_reads = set()
    with open(reads_to_taxid_location) as read_taxa_in:

        with open(fastq_reads) as fastq_reads_in:

            with open(out_file_loc, 'w') as out_file:
                header = read_taxa_in.readline()
                while True:
                    read_taxa1 = read_taxa_in.readline()
                    read_taxa2 = read_taxa_in.readline()
                    if not read_taxa2: break # EOF

                    fastq_read1 = [fastq_reads_in.readline().strip() for i in range(4)]
                    fastq_read2 = [fastq_reads_in.readline().strip() for i in range(4)]

                    read_taxa1 = read_taxa1.strip().split("\t")
                    read_taxa2 = read_taxa2.strip().split("\t")

                    read1_title = read_taxa1[0].strip()
                    read2_title = read_taxa2[0].strip()
                    read1_taxon_id = read_taxa1[1].strip()
                    read2_taxon_id = read_taxa1[1].strip()

                    if read1_title != fastq_read1[0] or read2_title != fastq_read2[0]:
                        print "ERROR: Please make sure that fastq_reads and read_to_taxid are in the same sorted order"
                        sys.exit()

                    if read1_taxon_id in taxon_hierarchy or read2_taxon_id in taxon_hierarchy:
                        matching_reads.add(read1_title)
                        matching_reads.add(read2_title)
                        out_file.write("\n".join(fastq_read1+fastq_read2)+"\n")

    return matching_reads


def is_taxon_id_in_nodes(taxon_id, taxon_nodes_dict):
    if taxon_id in taxon_nodes_dict.keys():
        return True
    else:
        return False


def get_required_reads_branched(reads_to_taxid_location, fastq_reads, taxon_id, taxon_nodes_dict, out_file_loc):
    assert type(taxon_id) is list, "taxon_id must be a list"
    assert type(reads_to_taxid_location) is str, "reads_to_taxid_location must be a string specifying file"

    taxon_id = set(taxon_id)
    matching_reads = set()
    matching_taxa = defaultdict(int)
    unfound_reads = 0

    with open(reads_to_taxid_location) as read_taxa_in:

        with open(fastq_reads) as fastq_reads_in:

            with open(out_file_loc, 'w') as out_file:
                read_taxa_in.readline()
                for line in read_taxa_in:
                    fastq_lines = [fastq_reads_in.readline().strip() for i in range(4)]
                    line = line.strip().split("\t")
                    read_title = line[0].strip()
                    read_taxon_id = line[1].strip()

                    if read_title != fastq_lines[0]:
                        print "ERROR: Please make sure that fastq_reads and read_to_taxid are in the same sorted order"
                        sys.exit()

                    try:
                        if is_child_taxon(read_taxon_id, taxon_nodes_dict, taxon_id):
                            matching_reads.add(read_title)
                            matching_taxa[read_taxon_id] += 1
                            out_file.write("\n".join(fastq_lines) + "\n")
                        else:
                            continue

                    except KeyError:
                        print "UNIDENTIFIED TAXON ID: " + read_taxon_id
                        unfound_reads += 1
                        continue

    print("Total Unclassified/Unknown Reads: %s" % unfound_reads)

    return matching_reads, matching_taxa


def get_required_reads_paired_branched(reads_to_taxid_location, fastq_reads, taxon_id, taxon_nodes_dict, out_file_loc):
    assert type(taxon_id) is list, "taxon_id must be a list"
    assert type(reads_to_taxid_location) is str, "reads_to_taxid_location must be a string specifying file"

    taxon_id = set(taxon_id)
    matching_reads = set()
    matching_taxa = defaultdict(int)
    unfound_reads = 0

    with open(reads_to_taxid_location) as read_taxa_in:

        with open(fastq_reads) as fastq_reads_in:

            with open(out_file_loc, 'w') as out_file:
                read_taxa_in.readline()
                for line in read_taxa_in:
                    fastq_lines = [fastq_reads_in.readline().strip() for i in range(4)]
                    line = line.strip().split("\t")
                    read_title = line[0].strip()
                    read_taxon_id = line[1].strip()

                    if read_title != fastq_lines[0]:
                        print "ERROR: Please make sure that fastq_reads and read_to_taxid are in the same sorted order"
                        sys.exit()

                    try:
                        if is_child_taxon(read_taxon_id, taxon_nodes_dict, taxon_id):
                            matching_reads.add(read_title)
                            matching_taxa[read_taxon_id] += 1
                            out_file.write("\n".join(fastq_lines) + "\n")
                        else:
                            continue

                    except KeyError:
                        print "UNIDENTIFIED TAXON ID: " + read_taxon_id
                        unfound_reads += 1
                        continue

    print("Total Unclassified/Unknown Reads: %s" % unfound_reads)

    return matching_reads, matching_taxa

def get_taxa_to_names(taxon_names_location):
    assert type(taxon_names_location) is str, "the taxon_names_location input must be a set of taxon_ids"

    taxa_to_names = {}

    with open(taxon_names_location) as names_in:
        for line in names_in:
            line = [field.strip() for field in line.strip().split("|")]
            #print "\t".join([line[0], line[1], line[3]])
            if line[3] == 'scientific name':
                taxa_to_names[line[0]] = line[1]

    return taxa_to_names


def print_hierarchy(taxon_hierarchy, taxa2names=None):
    assert type(taxon_hierarchy) is list, "the taxon hierarchy must be a list"

    level = 0
    for taxon in taxon_hierarchy[::-1]:
        indent = "".join(["     "]*level)
        if taxa2names:
            print indent+taxon_id_to_name(taxon, taxa2names)
        else:
            print indent+taxon
        level += 1


def taxon_id_to_name(taxon_id, taxa2names=None):

    if taxa2names:
        try:
            return taxa2names[taxon_id]
        except KeyError:
            return taxon_id+" (OLD ID - MERGED WITH SHOWN PARENT NODE)"
    else:
        return taxon_id



if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='fiter_reads_by_taxon.py is a simple program for filtering the reads '
                                                 'by taxon of interest. Use the -h flag for more information.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_reads',
                        help='The fastq file containing the reads of interest')

    parser.add_argument('read_to_taxid',
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-nodes','--taxon_nodes', required = False,
                        default = ["/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                                   "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('taxon_id', help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-ntaxa', '--number_of_parent_taxa', required=False,
                        help='Specify --parent_read_extract if you would like to filter the reads by every read that'
                             'is binned into each node in the hierarchy. Follow this flag with the location of the'
                             'NCBI Taxonomy Database that you would like to use to determine the hierarchy',
                        type=int, default=0)

    parser.add_argument('-names', '--use_taxon_names', required = False, help = 'FILL THIS OUT')

    parser.add_argument('-b', '--branched', action='store_true')

    parser.add_argument('-p', '--paired_ends', action='store_true', help= "Account for the assigned taxon for each read "
                                                                          "in the pair. If one passes the taxon test,"
                                                                          "it is included.")

    args = parser.parse_args()
    args = vars(args)

    fastq_reads = args['fastq_reads']
    read_to_taxid = args['read_to_taxid']
    taxon_id = args['taxon_id']
    taxon_nodes = args['taxon_nodes']
    ntaxa = args['number_of_parent_taxa']
    taxon_names = args['use_taxon_names']
    branched = args['branched']
    paired_ends =  args['paired_ends']


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
    print("\t"+taxon_id)
    if taxon_names: print taxon_id_to_name(taxon_id, taxa2names)

    print("Getting taxon hierarchy...")
    taxon_hierarchy = get_taxon_hierarchy(taxon_id, taxon_nodes_dict)


    print("Here is the taxon id hierarchy:")
    print_hierarchy(taxon_hierarchy, taxa2names)
    taxon_hierarchy = taxon_hierarchy[0:ntaxa+1]

    if not branched:

        out_file = "reads_filtered_%s_to_%s_ntaxa%d_LINEAR.fastq" % (taxon_hierarchy[0], taxon_hierarchy[-1], ntaxa)
        print("Collecting reads binned to the following taxa:")
        print_hierarchy(taxon_hierarchy, taxa2names)
        print("Writing out to file: %s" % out_file)
        if paired_ends:
            selected_reads = get_required_reads_paired_linear(read_to_taxid, fastq_reads, taxon_hierarchy, out_file)
        else:
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
        col_width_ids = max(len(str(max([int(taxon), int(children_taxa[taxon])]))) for taxon in children_taxa.keys()) + 2

        for child in children_taxa:
            print "".join([str(child).ljust(col_width_ids), str(children_taxa[child]).ljust(col_width_ids),
                          taxon_id_to_name(child, taxa2names).replace(" ","_").ljust(col_width_species)])