import objects

def read_fastq_paired_ends(file_object, lines_per_read=4):

    read = objects.pairedEnd([line.strip() for line in range(lines_per_read)],
                             [line.strip() for line in range(lines_per_read)])
    yield read


