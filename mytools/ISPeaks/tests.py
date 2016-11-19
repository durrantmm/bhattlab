import IO


def test_readers(gen1, gen2, class1, class2, is1, is2):
    line_start = 23
    gen1_in = IO.read_genome_alignment(open(gen1), line_start)
    gen2_in = IO.read_genome_alignment(open(gen2), line_start)

    is1_in = IO.read_insertion_alignments(open(is1), line_start)
    is2_in = IO.read_insertion_alignments(open(is2), line_start)

    class1_in = IO.read_classifications(open(class1), line_start)
    class2_in = IO.read_classifications(open(class2), line_start)
    print gen1_in.next()
    print gen2_in.next()

    print is1_in.next()
    print is2_in.next()

    print class1_in.next()
    print class2_in.next()


if __name__ == "__main__":
    gen1 = "data/fastq1_to_genome_bcaccae_sequence.sam"
    gen2 = "data/fastq2_to_genome_bcaccae_sequence.sam"
    is1 = "data/fastq1_to_IS.sam"
    is2 = "data/fastq2_to_IS.sam"
    class1 = "data/small_PE1.fq.results.tsv"
    class2 = "data/small_PE1.fq.results.tsv"

    test_readers(gen1, gen2, class1, class2, is1, is2)