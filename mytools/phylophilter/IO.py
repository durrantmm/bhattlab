import objects

def read_fastq_paired_ends_interleaved(fastq_file_object, lines_per_read=4):

    while True:
        try:
            read = objects.pairedEnd([fastq_file_object.readline().strip() for line in range(lines_per_read)],
                                     [fastq_file_object.readline().strip() for line in range(lines_per_read)])

            yield read
        except ValueError:
            break

def reads_to_taxids(reads_to_taxids_file_object, has_header=True):

    if has_header: reads_to_taxids_file_object.readline()

    while True:
        try:
            yield [reads_to_taxids_file_object.readline().strip(),
                   reads_to_taxids_file_object.readline().strip()]
        except ValueError:
            break

