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


def read_insertion_alignments(sam_file, sam_loc):

    while True:
        while True:
            try:
                first_line = sam_file.readline().strip().split()
                current_name = first_line[0]
                current_set = set([first_line[2]])

                #print first_line[0], first_line[2]

                for line in sam_file:
                    line = line.strip().split()

                    name = line[0]
                    if name == current_name:
                        #print line[0], line[2]
                        current_set.add(line[2])
                    else:
                        yield (current_name, current_set)
                        #print line[0], line[2]
                        current_name = name
                        current_set = set([line[2]])
            except IndexError:
                break
        yield (current_name.strip('@'), current_set)
        sam_file = open(sam_loc, 'r')

def read_insertion_alignments_once(sam_file):

    while True:
        try:
            first_line = sam_file.readline().strip().split()
            current_name = first_line[0]
            current_set = set([first_line[2]])

            #print first_line[0], first_line[2]

            for line in sam_file:
                line = line.strip().split()

                name = line[0]
                if name == current_name:
                    #print line[0], line[2]
                    current_set.add(line[2])
                else:
                    yield (current_name, current_set)
                    #print line[0], line[2]
                    current_name = name
                    current_set = set([line[2]])
        except IndexError:
            break
    yield (current_name.strip('@'), current_set)

