import argparse
import sys


output = False
read_set = set()


def sep_to_interleave(fastq_file1, fastq_file2, lines_per_leaf, output_file):

    with open(fastq_file1) as file_in1:

        with open(fastq_file2) as file_in2:

            with open(output_file, 'w') as out_file:

                while True:

                    read1 = [file_in1.readline().strip() for i in range(lines_per_leaf)]
                    read2 = [file_in2.readline().strip() for i in range(lines_per_leaf)]

                    if len(read2[0]) == 0 or len(read1[0]) == 0: break

                    out_file.write("\n".join(read1+read2)+"\n")


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Takes stacked reads and turns them into the interleaved format.'
                                                 'This will REMOVE any reads without a pair.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_files', nargs=2,
                        help='The two fastq files containing the STACKED reads of interest')
    parser.add_argument('-o', '--outfile', required=True,
                        help='Optional output specification.')
    parser.add_argument('-n', '--lines_per_leaf', type=int, required=False,
                        default=4,
                        help='The number of lines used per leaf in the output file. Default of 4 for standard fastq.')

    args = parser.parse_args()
    args = vars(args)

    fastq_file1, fastq_file2 = args['fastq_files']
    outfile = args['outfile']
    lines_per_leaf = args['lines_per_leaf']

    sep_to_interleave(fastq_file1, fastq_file2, lines_per_leaf, outfile)
    print("File written to %s" % outfile)

