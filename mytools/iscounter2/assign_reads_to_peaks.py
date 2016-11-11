import argparse, sys, os

def main(args):
    peaks = get_peaks(args['peaks_path'])
    sam = get_sam(args['sam_path'])

def get_sam(sam_path):
    sam = []
    with open(sam_path) as sam_in:
        for line in sam_in:
            line = line.strip().split()
            print line

    return sam


def get_peaks(peaks_path):
    peaks = []
    with open(peaks_path) as peaks_in:
        for line in peaks_in:
            line = line.strip().split()
            peaks.append((line[0],line[1]))

    return peaks



if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-s', '--sam_path', required=True,
                        help='The sam file of interest')
    parser.add_argument('-p', '--peaks_path', required=True,
                        help='The peaks file of interest')


    args = parser.parse_args()
    args = vars(args)

    main(args)

