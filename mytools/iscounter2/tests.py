from phylophilter import IO
import os, sys

def IO_get_insertion_alignments_TEST(sam_file):

    sam_dict = IO.get_insertion_alignments(sam_file)



if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "test_data")

    IO_get_insertion_alignments_TEST(os.path.join(data_dir, "Bacteroides_all.fasta.sam"))

