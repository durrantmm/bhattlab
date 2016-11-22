import macs2
import pysam
from os.path import basename, join
from glob import glob
import sys
import IO
from collections import defaultdict
from operator import itemgetter

def call_all_peaks(version, bamdict, outdir, state):
    for key in bamdict:
        bam = bamdict[key]
        handle = pysam.AlignmentFile(bam, "rb")
        genome_len = handle.header['SQ'][0]['LN']
        read_count = sum([1 for read in handle])
        if read_count < 10:
            state.logger.info("Too few reads to perform peak calling in %s" %
                              "-".join(basename(bam).split(state.settings.path_delim)))
            continue

        state.paths.peak_paths[key] = macs2.call_peaks(version, bam, genome_len, outdir)

def process_peaks_indiv(state):
    final_results = []
    for key in state.paths.peak_paths:
        path = state.paths.peak_paths[key]

        peaks = []
        with open(path) as infile:
            for line in infile:
                line = line.strip().split()
                genome_frag, start, stop = line[0], int(line[1]), int(line[2])
                peaks.append([genome_frag, start, stop])

        peak_results = defaultdict(int)
        for read in IO.read_genome_alignment(open(state.paths.taxon_sam_paths[key]), 1):
            for aln in read:
                for peak in peaks:
                    if aln['RNAME'] == peak[0] and is_within_peak(int(aln['POS']), peak[1], peak[2], state.settings.peak_extension):
                        peak_results[state.settings.path_delim.join([str(peak[0]), str(peak[1]), str(peak[2])])] += 1

        for result in peak_results:
            final_results.append(key.split(state.settings.path_delim) +
                                 result.split(state.settings.path_delim) +
                                 [str(peak_results[result])])

    final_results = sorted(final_results, key=(itemgetter(0,1,2)))
    final_results.insert(0, ['Genome', 'TaxonID', 'IS', 'GenomeFrag', 'PeakStart', 'PeakEnd', 'NumFlankingReads'])

    open(join(state.paths.results_dir, 'indiv_results.tsv'),'w').write('\n'.join(['\t'.join(line) for line in final_results]))

def is_within_peak(pos, peak_start, peak_end, extension):
    dist_to_peak = sys.maxint

    if pos > peak_start - extension and pos < peak_end + extension:
        return True

    return False
