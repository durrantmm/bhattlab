import argparse
import sys, os


if __name__ == "__main__":

    print os.path.realpath(__file__)
    sys.exit()
    # setup the option parser
    parser = argparse.ArgumentParser(
        description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-fq', '--fastq_reads', required=True,
                        help='This is a fastq file containing PAIRED END reads that are in an interleaved format.')

    parser.add_argument('-b', '--read_to_taxid', required=True,
                        help='A tab-separated file where the first column is the read title and the second'
                             'column is the assigned taxon id')

    parser.add_argument('-t', '--taxon_id', required=True,
                        help='The NCBI Taxon ID of the species of interest')

    parser.add_argument('-nodes', '--taxon_nodes', required=False, type=list,
                        default=[
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('-is', '--insertion_sequences', required=False, type=list,
                        default=[
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/nodes.dmp",
                            "/srv/gsfs0/projects/bhatt/mdurrant/my_code/bhattlab/mytools/TaxonomyDatabase/merged.dmp"],
                        help='Location of the NCBI Taxonomy Database nodes.txt file', nargs='*')

    parser.add_argument('-o', '--output_file', required=False,
                        help='Specify the output file')

    args = parser.parse_args()
    args = vars(args)


