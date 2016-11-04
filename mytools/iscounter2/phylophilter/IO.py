import shared_objects, sys
from collections import defaultdict

def read_fastq_paired_ends_interleaved(fastq_file_object, lines_per_read=4):

    while True:
        try:
            read = shared_objects.pairedEndRead([fastq_file_object.readline().strip() for line in xrange(lines_per_read)],
                                                [fastq_file_object.readline().strip() for line in xrange(lines_per_read)])

            yield read
        except ValueError:
            break

def read_fastq_non_paired(fastq_file_object, lines_per_read=4):

    while True:
        try:
            read = shared_objects.singleRead([fastq_file_object.readline().strip() for line in xrange(lines_per_read)])

            yield read
        except ValueError:
            break

def paired_reads_to_taxids(reads_to_taxids_file_object, has_header=True, delim='\t'):

    if has_header: reads_to_taxids_file_object.readline()

    while True:
        try:
            read_class = shared_objects.pairedEndClassification(
                reads_to_taxids_file_object.readline().strip().split(delim),
                reads_to_taxids_file_object.readline().strip().split(delim))
            yield read_class
        except ValueError:
            break

def non_paired_reads_to_taxids(reads_to_taxids_file_object, has_header=True, delim='\t'):

    if has_header: reads_to_taxids_file_object.readline()

    while True:
        try:
            read_class = shared_objects.singleReadClassification(
                reads_to_taxids_file_object.readline().strip().split(delim))
            yield read_class
        except ValueError:
            break


def get_insertion_alignments(sam_file):
    has_header = False
    with open(sam_file, 'r') as file_in:
        if file_in.readline()[0] == '@': has_header = True

    out_dict = defaultdict(set)
    with open(sam_file, 'r') as file_in:

        if has_header: remove_sam_header(file_in)

        for line in file_in:
            line = line.strip().split()
            name = line[0]
            mapping = line[2]

            out_dict[name].add(mapping)

    return dict(out_dict)

def remove_sam_header(sam):

    for line in sam:
        if line.startswith("@PG"):
            break
        else:
            continue
