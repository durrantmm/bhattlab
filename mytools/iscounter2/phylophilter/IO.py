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


def get_insertion_alignments(sam_file, has_header=True):

    if has_header: remove_sam_header(sam_file)

    while True:
        line = sam_file.readline().strip().split()
        name = line[0]
        ISs = set()
        try:
            while len(line[0]) != 0:
                while line[0] != name:
                    ISs.add(line[2])
                    line = sam_file.readline().strip().split()
                name = line[0]
                yield [name, ISs]

            raise IndexError()

        except IndexError:
            break

def remove_sam_header(sam):
    line = sam.readline()
    while not line.startswith("@PG"):
        sam.readline()