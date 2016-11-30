import os, sys
import time
from os.path import basename
from collections import defaultdict
from glob import glob
import samtools, peaks
import shared

def action(state):

    logger = state.logger
    logger.info("Loading taxonomy nodes and ranks from specified file...")
    nodes, ranks = shared.get_taxon_nodes_ranks(state.paths.taxon_nodes)
    state.settings.set_nodes(nodes)
    state.settings.set_ranks(ranks)

    logger.info("Loading taxonomy names from specified file...")
    state.settings.set_names(shared.get_taxon_names(state.paths.taxon_names))

    logger.info("Collecting all sam file information...")
    collect_bam_info(state)

    logger.info("Merging all of the concordant sam files between samples...")
    samtools.merge_bam_files(state)

    logger.info("Beginning peak calling...")
    logger.info("Converting all sam files to bam, sorting and indexing...")
    samtools.process_all_taxon_sams(state)

    logger.info("Calling insertion peaks for each individual merged bam file...")
    peaks.call_all_peaks('2.1.1.20160309', state.paths.merged_bam_paths, state.paths.merged_peaks_paths,
                         state.paths.merged_peaks_dir, state)

    logger.info("Processing the merged peaks at an individual taxon level...")
    peaks.process_peaks_indiv(state.paths.merged_peaks_paths, state.paths.bam_info, state.paths.merged_indiv_peaks_path,
                              state)

    logger.info("Saved the results to %s" % basename(state.paths.merged_indiv_peaks_path))


    sys.exit()

    if not state.settings.num_reads:
        logger.info("Counting the number of reads in the given FASTQ file...")
        state.settings.num_reads = misc.count_lines(open(state.paths.class_files[0]), skip_header=True)
        logger.info("File contains %d reads" % state.settings.num_reads)



    logger.info("Loading taxonomy names from specified file...")
    state.settings.set_names(shared.get_taxon_names(state.paths.taxon_names))

    logger.info("Aligning the FASTQ files to the insertion sequences...")

    logger.info("Building the insertion fasta file for alignment...")
    bowtie2.build('2.2.9', state.paths.insertion_fasta)

    logger.info("Aligning the forward reads in %s to the file %s" %
                (basename(state.paths.fastq_files[0]), basename(state.paths.insertion_fasta)))
    outsam_fq1 = bowtie2.align_fastq_to_insertions('2.2.9',
                                                   state.paths.insertion_fasta,
                                                   state.paths.fastq_files[0],
                                                   state.paths.fastq_to_IS_algnmnts[0],
                                                   state.settings.threads)

    logger.info("Output saved to %s" % basename(state.paths.fastq_to_IS_algnmnts[0]))

    logger.info("Aligning the reverse reads in %s to the file %s" %
                (basename(state.paths.fastq_files[1]), basename(state.paths.insertion_fasta)))
    outsam_fq2 = bowtie2.align_fastq_to_insertions('2.2.9',
                                                   state.paths.insertion_fasta,
                                                   state.paths.fastq_files[1],
                                                   state.paths.fastq_to_IS_algnmnts[1],
                                                   state.settings.threads)
    logger.info("Output saved to %s" % basename(state.paths.fastq_to_IS_algnmnts[1]))

    tic = time.clock()
    logger.info("Beginning alignment to all specified reference files...")
    align_to_references(state)
    toc = time.clock()
    logger.debug("Time to align to genome: %s" % (toc-tic))

    logger.info("Creating taxon-to-insertion sam files containing all insertion-flanking-reads...")
    sorted_dict = phylosorter.sort_flanking_reads(state)

    logger.info("Consolidating resulting sam files...")
    misc.consolidate_taxon_sams(state)

    logger.info("%d distinct sam files created containing genome-specific, taxon-sorted, IS-flanking reads..." %
                len(state.paths.taxon_sam_paths))

    if state.settings.merge_subspecies:
        logger.info("Merging sams with species-subspecies relationship for downstream analysis...")
        misc.merge_subspecies_sams(state)


    stats_path = os.path.join(state.paths.out_dir, 'flanking_reads_stats.tsv')
    logger.info("Writing the stats out to file %s..." % stats_path)
    open(stats_path, 'w').write(
        phylosorter.sorted_flanks_dict_to_string(state.settings.taxon_reads_dict, state.settings.taxon_names))

    logger.info("Beginning peak calling...")
    logger.info("Converting all sam files to bam, sorting and indexing...")
    samtools.process_all_taxon_sams(state)

    logger.info("Calling insertion peaks for each individual bam file...")
    peaks.call_all_peaks('2.1.1.20160309', state.paths.taxon_bam_paths, state.paths.single_peak_paths, state.paths.single_peaks_dir, state)

    logger.info("Processing the peaks at an individual taxon level...")
    peaks.process_peaks_indiv(state.paths.single_peak_paths, state.paths.taxon_sam_paths, state.paths.indiv_results_out, state)
    logger.info("Saved the results to %s" % basename(state.paths.indiv_results_out))

    logger.info("Processing the peaks by taxonomy traversal...")
    peaks.process_peaks_taxonomy_traversal(state.paths.single_peak_paths, state.paths.taxon_sam_paths,
                                           state.paths.taxonomy_traversal_results_out, state)
    logger.info("Saved the results to %s" % basename(state.paths.taxonomy_traversal_results_out))

    logger.info("Analysis Complete :)")

def collect_bam_info(state):

    bam_info = defaultdict(lambda: defaultdict(str))
    for dir in state.paths.ispeaks_dirs:
        sam_dir = os.path.join(dir, 'sams', 'taxon_sorted_sams_dir')
        if not os.path.isdir(sam_dir):
            raise TypeError("The directory architecture of the ISPeaks folder %s is unexpected." % basename(dir))

        for sam in glob(sam_dir+'/*.bam'):
            key = '.'.join(basename(sam).split('.')[:-1])
            bam_info[key][dir] = sam

    state.paths.bam_info = bam_info

