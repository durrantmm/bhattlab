import shared_objects, sys
from collections import defaultdict, OrderedDict


def read_genome_alignment(sam_file):
    sam_header = ['QNAME', 'FLAG', 'RNAME', 'POS', 'MAPQ', 'CIGAR', 'RNEXT', 'PNEXT', 'TLEN', 'SEQ', 'QUAL']
    while True:
        try:

            first_line = OrderedDict(zip(sam_header, sam_file.readline().strip().split()))
            current_name = first_line['QNAME']
            current_set = [first_line]

            for line in sam_file:
                line = OrderedDict(zip(sam_header, line.strip().split()))

                name = line['QNAME']
                if name == current_name:
                    current_set.append(line)
                else:
                    yield current_set
                    current_name = name
                    current_set = [line]

        except KeyError:
            break

    yield current_set

def read_insertion_alignments_looped(sam_file):
    sam_header = ['QNAME', 'FLAG', 'RNAME', 'POS', 'MAPQ', 'CIGAR', 'RNEXT', 'PNEXT', 'TLEN', 'SEQ', 'QUAL']

    while True:
        try:

            first_line = dict(zip(sam_header, sam_file.readline().strip().split()))
            current_name = first_line['QNAME']
            current_set = [first_line]

            for line in sam_file:
                line = dict(zip(sam_header, line.strip().split()))

                name = line['QNAME']
                if name == current_name:
                    current_set.append(line)
                else:
                    yield current_set
                    current_name = name
                    current_set = [line]

        except KeyError:
            break

    yield current_set

def read_classifications(read_class_file, delim='\t'):
    header = ''
    header = read_class_file.readline().strip().split('\t')
    for title in range(len(header)):
        header[title] = header[title].replace(' ', '').upper()

    while True:
        try:
            read_class = dict(zip(header, read_class_file.readline().strip().split('\t')))
            read_class['HEADER'] = read_class['HEADER'].split()[0].strip('@')
            yield read_class
        except ValueError:
            break


# OLD STUFF FOR REFERENCE
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

