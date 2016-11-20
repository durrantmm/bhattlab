import sys, os
from glob import glob
import bowtie2
import phylosorter, misc
from os.path import basename

def exec_single(state):

    logger = state.logger
    if not state.settings.num_reads:
        logger.info("Counting the number of reads in the given FASTQ file...")
        state.settings.num_reads = misc.count_lines(open(state.paths.class_files[0]), skip_header=True)
        logger.info("File contains %d reads" % state.settings.num_reads)


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

    logger.info("Beginning alignment to all specified reference files...")
    align_to_references(state)

    logger.info("Creating taxon-to-insertion sam files containing all insertion-flanking-reads...")
    sorted_dict = phylosorter.sort_flanking_reads(state)

    logger.info("Consolidating resulting sam files...")
    misc.consolidate_sams(state.paths.taxon_sorted_sams_dir, '-::-')
    logger.info("%d distinct sam files created containing genome-specific, taxon-sorted, IS-flanking reads..." %
                len(glob(state.paths.taxon_sorted_sams_dir+'/*')))



    os.path.join(state.paths.out_dir, 'flanking_reads_stats.tsv')

    logger.info("Analysis Complete :)")


def align_to_references(state):
    logger = state.logger

    ref_sams = {}

    for refpath in state.paths.reference_genomes:
        suffix = basename(refpath).split('.')[0]

        logger.info("Building the genome fasta file for the file %s..." % basename(refpath))
        bowtie2.build('2.2.9', refpath, logger)

        logger.info("Aligning the forward reads in %s to the genome %s..." %
                    (basename(state.paths.fastq_files[0]), basename(refpath)))
        outsam1 = bowtie2.align_to_genome('2.2.9',
                                          refpath,
                                          state.paths.fastq_files[0],
                                          os.path.join(state.paths.full_sams_dir, 'fastq1_to_genome_%s.sam' % suffix),
                                          state.settings.threads)
        logger.info("Output saved to %s" % basename(outsam1))

        logger.info("Aligning the reverse reads in %s to the genome %s..."%
                    (basename(state.paths.fastq_files[1]), basename(refpath)))
        outsam2 = bowtie2.align_to_genome('2.2.9',
                                          refpath,
                                          state.paths.fastq_files[1],
                                          os.path.join(state.paths.full_sams_dir, 'fastq2_to_genome_%s.sam' % suffix),
                                          state.settings.threads)
        logger.info("Output saved to %s" % basename(outsam2))

        ref_sams[refpath] = (outsam1, outsam2)
        state.paths.fastq_to_genome_algnmnts = ref_sams

    return ref_sams