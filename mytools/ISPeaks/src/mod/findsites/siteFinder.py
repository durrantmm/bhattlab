import sys
import shared
from genome import GenomeAlignment
from peakQC import PeakQC

class SiteFinder:

    def __init__(self, bam_file, peaks_path, logger=None):

        self.log = logger

        self.bam_file = bam_file
        self.peaks_path = peaks_path
        self.peaks = shared.get_peaks(peaks_path)

        self.genome = None
        self.peakQC = None

    def find_sites(self):

        self.log_info("Building the genome read depth model...")
        self.genome = GenomeAlignment(self.bam_file, self.peaks, self.log)
        self.genome.generateModel()
        self.log_debug("Finished building the genome model...")

        self.log_debug("Creating the PeakQC object...")
        self.peakQC = PeakQC(self.genome, self.peaks, self.log)

        for chrom, start_zeroi, end_zeroi in self.peaks:
            peak_str = shared.peak_str(start_zeroi, end_zeroi)

            if self.log: self.log.info("Processing the peak %s..." % peak_str)
            self.peakQC.perform_peak_QC(chrom, start_zeroi, end_zeroi)



            continue


            max_depth = max(self.forward_read_count[chrom][start_zeroi:end_zeroi+1] + self.reverse_read_count[chrom][start_zeroi:end_zeroi+1])
            forward_maxima = self.get_maxima(self.forward_read_count, chrom, start_zeroi, end_zeroi, max_depth, lower_peak_cutoff_perc)
            reverse_maxima = self.get_maxima(self.reverse_read_count, chrom, start_zeroi, end_zeroi, max_depth, lower_peak_cutoff_perc)
            print start_zeroi + 1
            print end_zeroi + 1
            print ', '.join([str(i) for i in forward_maxima])
            print ', '.join([str(i) for i in reverse_maxima])

        self.peakQC.print_QC_log()
        sys.exit()

            #target_site = self.find_target_site(chrom, start_zeroi, end_zeroi)


    def log_info(self, string):
        if self.log:
            self.log.info(string)


    def log_debug(self, string):
        if self.log:
            self.log.debug(string)