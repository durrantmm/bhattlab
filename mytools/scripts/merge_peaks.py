import sys


peaks1 = sys.argv[1]
peaks2 = sys.argv[2]

with open(peaks1) as peaks_in:
    for line in peaks_in:
        print line