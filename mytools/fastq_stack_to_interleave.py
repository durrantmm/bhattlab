import argparse


def destack_and_interleave(fastq_file):

    read_set = set()
    with open(fastq_file) as file_in:
        for line in file:
            line = line.strip().split()
            if line[0][0] == '@':
                print line


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Takes stacked reads and turns them into the interleaved format.'
                                                 'This will REMOVE any reads without a pair.')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('fastq_file',
                        help='The fastq file containing the STACKED reads of interest')


    args = parser.parse_args()
    args = vars(args)

    fastq_file = args['fastq_file']

    destack_and_interleave(fastq_file)

