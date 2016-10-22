import argparse
import sys

output = False
read_set = set()


def destack_and_interleave(fastq_file, part_B_line):

    with open(fastq_file) as file_in1:

        with open(fastq_file) as file_in2:

            line_number = 1
            while line_number < part_B_line:
                file_in1.readline()
                line_number += 1

            with open(".".join(fastq_file.split(".")[:-1]+["INTERLEAVED",fastq_file.split(".")[-1]]), 'w') as out_file:
                read1 = ["GO"]
                while True:
                    try:
                        read1 = [file_in2.readline().strip() for i in range(4)]
                        read2 = [file_in1.readline().strip() for i in range(4)]

                        test = read1[0].split()[0]

                        print("\n".join(read1))
                        print("\n".join(read2))

                    except IndexError:
                        break

if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Takes stacked reads and turns them into the interleaved format.'
                                                 'This will REMOVE any reads without a pair.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_file',
                        help='The fastq file containing the STACKED reads of interest')
    parser.add_argument('part_B_line', type=int,
                        help='The line in the file where the second reads are first begin, (1-indexed).')


    args = parser.parse_args()
    args = vars(args)

    fastq_file = args['fastq_file']
    part_B_line = args['part_B_line']

    destack_and_interleave(fastq_file, part_B_line)

