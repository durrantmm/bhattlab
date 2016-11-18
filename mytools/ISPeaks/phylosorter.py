import os, sys
import misc, IO
from itertools import izip
from collections import defaultdict

ref_count = 0

def sort_flanking_reads(fq1_to_is_path, fq2_to_is_path, class1_path, class2_path, ref_sams, outdir, logger=None):
    global ref_count
    sorted_dir = os.path.join(outdir, 'sorted_sams')
    misc.makedir(outdir)

    classif1, classif2 = IO.read_classifications(open(class1_path)), IO.read_classifications(open(class2_path))
    IS_sam1, IS_sam2 = IO.read_insertion_alignments_looped(open(fq1_to_is_path)), IO.read_insertion_alignments_looped(open(fq2_to_is_path))

    for ref in ref_sams:
        ref_count += 1
        genome_sam1, genome_sam2 = IO.read_genome_alignment(open(ref_sams[ref][0])), IO.read_genome_alignment(open(ref_sams[ref][1]))

        filter_flanks_to_fastq((genome_sam1, genome_sam2), (classif1, classif2), (IS_sam1, IS_sam2), ref, logger)


def filter_flanks_to_fastq(genome_sams, classifs, IS_sams, ref, logger=None):

    flank_sams_out = {}

    loop_count = 0
    total_read_count = 0
    flanking_reads_count = 0

    if logger: logger.info("Beginning read filtering...")

    for genome_aln1, genome_aln2, IS_aln1, IS_aln2, class1, class2 in izip(genome_sams[0], genome_sams[1], IS_sams[0], IS_sams[1], classifs[0], classifs[1]):
        total_read_count += 1

        loop_count = misc.loop_counter(loop_count, total_read_count, logger)

        # Check the reads and the classifications align
        check_matching_reads(genome_aln1, genome_aln2, IS_aln1, IS_aln2, class1, class2)

        if is_aligned(IS_aln1[0]) and is_aligned(IS_aln2[0]):
            pass
        elif is_aligned(genome_aln1[0]) and is_aligned(IS_aln2[0]):
            write_aln(genome_aln1, IS_aln2, ref, flank_sams_out)
        elif is_aligned(IS_aln1[0]) and is_aligned(genome_aln2[0]):
            write_aln(genome_aln2, IS_aln1, ref, flank_sams_out)
        else:
            continue

        # print [val for key, val in genome_aln1[0].items()]

    logger.info("Total reads counted: %d" % total_read_count)
    logger.info("Total flanking reads meeting criteria: %d" % flanking_reads_count)

def check_matching_reads(genome_aln1, genome_aln2, IS_aln1, IS_aln2, class1, class2):
    if genome_aln1[0]['QNAME'] == genome_aln2[0]['QNAME'] == IS_aln1[0]['QNAME'] == IS_aln2[0]['QNAME'] == class1['HEADER'] == class2['HEADER']:
        pass
    else:
        raise IndexError("The reads and the classifications need to be in the same order.")

def is_aligned(alignment):
    if alignment['RNAME'] == '*':
        return False
    else:
        return True

def write_aln(gen_algnmnts, IS_algnmnts, ref, sams_out):
    global ref_count

    for gen_aln in gen_algnmnts:
        for IS_aln in IS_algnmnts:
            IS = IS_aln['RNAME']
            print ref, IS
    sys.exit()
