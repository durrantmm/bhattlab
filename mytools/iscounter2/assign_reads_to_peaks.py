import argparse, sys, os

def main(args):
    peaks, peaks_dict = get_peaks(args['peaks_path'])
    sam = get_sam(args['sam_path'])


    for read in sam:
        pos = int(sam[3])
        nearest_peak = get_nearest_peak(pos, peaks)
        peaks_dict[nearest_peak] += 1

    print peaks_dict

def get_nearest_peak(pos, peaks):
    nearest_peak = sys.maxint
    for peak in peaks:
        if abs(pos-peak[0]) < nearest_peak or abs(pos-peak[1]) < nearest_peak:
            nearest_peak = "-".join([str(peak[0]), str(peak[1])])
    return nearest_peak

def get_sam(sam_path):
    sam = []
    with open(sam_path) as sam_in:
        for line in sam_in:
            line = line.strip().split()
            sam.append(line)

    return sam


def get_peaks(peaks_path):
    peaks = []
    peaks_dict = {}
    with open(peaks_path) as peaks_in:
        for line in peaks_in:
            line = line.strip().split()
            peaks.append((int(line[0]), int(line[1])))
            peaks_dict["-".join([line[0],line[1]])] = 0

    return peaks, peaks_dict



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

