from collections import defaultdict
import shared
from peakAnalyzer import PeakAnalyzer
class PeakQC:

    def __init__(self, genome, peaks, logger=None):
        self.log = logger

        self.QC_log = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        self.genome = genome
        self.peaks = peaks


        ## PEAK ANALYZER
        self.peak_analyzer = PeakAnalyzer(self.genome, self.peaks, self.log)


        ## QC TAGS
        self.depth_tag = "MAX_DEPTH"
        self.exist_maxima_tag = "EXIST_MAXIMA"
        self.paired_maxima_tag = "N_PAIRED_MAXIMA"
        self.mult_insertions_tag = "MULTIPLE_INSERTIONS"



    def perform_peak_QC(self, chrom, start, end):

        self.perform_depth_QC(chrom, start, end)
        self.perform_exist_maxima_QC(chrom, start, end)
        self.perform_paired_maxima_QC(chrom, start, end)



    def perform_depth_QC(self, chrom, start, end):
        peak_str = shared.peak_str(start, end)
        max_depth = max(self.genome.forward_depth[chrom][start:end + 1] +
                        self.genome.reverse_depth[chrom][start:end + 1])

        if max_depth < 20:
            self.QC_log[chrom][peak_str][self.depth_tag] = 'LOW'
        elif max_depth < 50:
            self.QC_log[chrom][peak_str][self.depth_tag] = 'MED'
        else:
            self.QC_log[chrom][peak_str][self.depth_tag] = 'HIGH'


    def perform_exist_maxima_QC(self, chrom, start, end):
        peak_str = shared.peak_str(start, end)

        if len(self.peak_analyzer.peak_maxima[chrom][peak_str]['FORWARD']) == 0 and \
                        len(self.peak_analyzer.peak_maxima[chrom][peak_str]['REVERSE']) == 0:
            self.QC_log[chrom][peak_str][self.exist_maxima_tag] = 'FALSE'

        elif len(self.peak_analyzer.peak_maxima[chrom][peak_str]['FORWARD']) == 0:
            self.QC_log[chrom][peak_str][self.exist_maxima_tag] = 'MISSING_FORWARD'

        elif len(self.peak_analyzer.peak_maxima[chrom][peak_str]['REVERSE']) == 0:
            self.QC_log[chrom][peak_str][self.exist_maxima_tag] = 'MISSING_REVERSE'

        else:
            self.QC_log[chrom][peak_str][self.exist_maxima_tag] = 'TRUE'



    def perform_paired_maxima_QC(self, chrom, start, end):
        peak_str = shared.peak_str(start, end)
        self.peak_analyzer




    ### Output Functions
    def print_QC_log(self):
        print '\t'.join(["CHROM", "PEAK", self.depth_tag, self.exist_maxima_tag, self.paired_maxima_qc])

        for chrom, start, end in self.peaks:
            peak_str = shared.peak_str(start, end)

            out_list = [chrom, peak_str]
            out_list.append(self.QC_log[chrom][peak_str][self.depth_tag])
            out_list.append(self.QC_log[chrom][peak_str][self.exist_maxima_tag])
            out_list.append(self.QC_log[chrom][peak_str][self.paired_maxima_tag])

            print "\t".join(out_list)

