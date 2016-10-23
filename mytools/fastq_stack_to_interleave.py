import argparse
import sys

output = False
read_set = set()


def destack_and_interleave(fastq_file, part_B_line, lines_per_leaf, output_file):

    with open(fastq_file) as file_in1:

        with open(fastq_file) as file_in2:

            line_number = 1
            while line_number < part_B_line:
                file_in1.readline()
                line_number += 1

            with open(output_file, 'w') as out_file:

                while True:

                    try:
                        read1 = [file_in2.readline().strip() for i in range(lines_per_leaf)]
                        read1[0][0] # Error Test
                        read2 = [file_in1.readline().strip() for i in range(lines_per_leaf)]
                        read2[0][0]  # Error Test

                        out_file.write("\n".join(read1 + read2) + "\n")
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
    parser.add_argument('-o', '--outfile', required=False,
                        help='Optional output specification.')
    parser.add_argument('-n', '--lines_per_leaf', type=int, required=False,
                        default=4,
                        help='The number of lines used per leaf in the output file. Default of 4 for standard fastq.')

    args = parser.parse_args()
    args = vars(args)

    fastq_file = args['fastq_file']
    part_B_line = args['part_B_line']
    outfile = args['outfile']
    lines_per_leaf = args['lines_per_leaf']

    if outfile is None: outfile = ".".join(fastq_file.split(".")[:-1]+["INTERLEAVED",fastq_file.split(".")[-1]])

    destack_and_interleave(fastq_file, part_B_line, lines_per_leaf, outfile)
    print("File written to %s" % outfile)

