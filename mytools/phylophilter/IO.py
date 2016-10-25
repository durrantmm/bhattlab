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
        read1 = reads_to_taxids_file_object.readline().strip()
        read2 = reads_to_taxids_file_object.readline().strip()
        if len(read1) == 0 or len(read2) == 0: break
        yield [read1.split('\t'), read2.split('\t')]


