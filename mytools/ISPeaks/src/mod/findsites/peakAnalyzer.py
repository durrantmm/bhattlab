from collections import defaultdict
import shared
import sys

class PeakAnalyzer:
    def __init__(self, genome, peaks, logger=None):

        self.log = logger

        self.peaks = peaks
        self.genome = genome

        self.peak_pairs = defaultdict(lambda: defaultdict(list))
        self.peak_maxima = defaultdict(lambda: defaultdict(list))
        self.calc_maxima_forward_reverse_all_peaks()



    def calc_maxima_forward_reverse_all_peaks(self):
        self.log_info("Calculating the forward and reverse maxima for each of the peak regions...")

        self.peak_maxima = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for chrom, start, end in self.peaks:
            peak_str = shared.peak_str(start, end)
            self.log_debug("Calculating maxima for peak %s..." % peak_str)


            max_depth = max_depth = max(self.genome.forward_depth[chrom][start:end + 1] +
                        self.genome.reverse_depth[chrom][start:end + 1])

            forward = self.get_maxima_single(self.genome.forward_depth, chrom, start, end, max_depth)
            reverse = self.get_maxima_single(self.genome.reverse_depth, chrom, start, end, max_depth)

            self.peak_maxima[chrom][peak_str]["FORWARD"] = forward
            self.peak_maxima[chrom][peak_str]["REVERSE"] = reverse
            self.log_debug("Forward Maxima: %s" % shared.pprint_list(forward))
            self.log_debug("Reverse Maxima: %s" % shared.pprint_list(reverse))

            peak_pairs = self.calc_peak_pairs_single(forward, reverse)
            self.log_debug("Peak Pairs: %s" % shared.pprint_list(peak_pairs))
            self.peak_pairs[chrom][peak_str] = peak_pairs



    def calc_peak_pairs_single(self, forward_peaks, reverse_peaks):
        merged_peaks = sorted(forward_peaks + reverse_peaks)
        peak_pairs = []

        p = 0
        while p+1 < len(merged_peaks):
            if merged_peaks[p] in forward_peaks and merged_peaks[p+1] in reverse_peaks:
                peak_pairs.append((merged_peaks[p], merged_peaks[p+1]))
                p += 2
            else:
                p += 1
        return peak_pairs


    def get_maxima_single(self, read_counts, chrom, start_zeroi, end_zeroi, max_depth, lower_peak_cutoff_perc=0.25, minimum_peak_width=30):

        depth_cutoff = int(lower_peak_cutoff_perc * max_depth)

        maxima = []
        current_max_depth = 0
        current_max_pos = 0
        in_peak = False
        current_peak_width = 1

        for pos in range(start_zeroi, end_zeroi+1):
            pos_depth = read_counts[chrom][pos]

            if in_peak:
                current_peak_width += 1

            if pos_depth > depth_cutoff:
                if in_peak == False:
                    in_peak = True
                    current_peak_width = 1

                if pos_depth > current_max_depth:
                    current_max_depth = pos_depth
                    current_max_pos = pos

            else:
                if in_peak == True:
                    if current_peak_width > minimum_peak_width:
                        maxima.append(current_max_pos)
                    current_max_depth = 0
                    current_max_pos = 0
                    in_peak = False


        if in_peak == True:
            if current_peak_width > minimum_peak_width:
                maxima.append(current_max_pos)
            current_max_depth = 0
            current_max_pos = 0
            in_peak = False

        return maxima


    def get_maxima_forward_reverse_all_peaks(self, peaks):
        if not self.peak_maxima:
            self.peak_maxima = self.calc_maxima_forward_reverse_all_peaks()

        return self.peak_maxima


    def get_peak_pairs(self, peaks):
        if not self.peak_pairs:
            self.peak_pairs = self.calc_maxima_forward_reverse_all_peaks()

        return self.peak_pairs


    ## LOGGER WRAPPERS
    def log_info(self, string):
        if self.log:
            self.log.info(string)

    def log_debug(self, string):
        if self.log:
            self.log.debug(string)



