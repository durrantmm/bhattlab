import objects

def read_fastq_paired_ends_interleaved(fastq_file_object, lines_per_read=4):

    while True:
        read = objects.pairedEnd([fastq_file_object.readline().strip() for line in range(lines_per_read)],
                                 [fastq_file_object.readline().strip() for line in range(lines_per_read)])
        yield read


