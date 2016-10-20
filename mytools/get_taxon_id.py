import argparse
import sys
from collections import defaultdict

# start here when the script is launched


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('name', help='FILL THIS OUT')
    parser.add_argument('-names','--taxon_names_location', required = False,
                        default="/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/names.dmp",
                        help='FILL THIS OUT')



    args = parser.parse_args()
    args = vars(args)

    name = args['name'].upper().split()
    taxon_names_location = args['taxon_names_location']



    with open(taxon_names_location) as names_in:
        for line in names_in:
            line = [field.strip() for field in line.strip().split("|")]

            for part in name:
                print part
                if part not in line[1].upper():
                    break
            else:
                print("Name: %s; Taxon ID: %s" % (line[1], line[0]))







