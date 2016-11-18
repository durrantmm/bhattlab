import os, sys
import misc, IO
from itertools import izip
from collections import defaultdict

complete_class_exclusions = []
genome_class_exclusions = []
IS_class_exclusions = []

def sort_flanking_reads(fq1_to_is_path, fq2_to_is_path, class1_path, class2_path, ref_sams, outdir, logger=None):
    sorted_dir = os.path.join(outdir, 'sorted_sams')
    misc.makedir(sorted_dir)

    classif1, classif2 = IO.read_classifications(open(class1_path)), IO.read_classifications(open(class2_path))
    IS_sam1, IS_sam2 = IO.read_insertion_alignments_looped(open(fq1_to_is_path)), IO.read_insertion_alignments_looped(open(fq2_to_is_path))

    for ref in ref_sams:
        genome_sam1, genome_sam2 = IO.read_genome_alignment(open(ref_sams[ref][0])), IO.read_genome_alignment(open(ref_sams[ref][1]))

        filter_flanks_to_fastq((genome_sam1, genome_sam2), (classif1, classif2), (IS_sam1, IS_sam2), ref, sorted_dir, logger)

    return sorted_dir


def filter_flanks_to_fastq(genome_sams, classifs, IS_sams, ref, outdir, logger=None):
    global complete_class_exclusions, genome_class_exclusions, IS_class_exclusions

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
        if not passes_complete_class_exclusions(class1, class2):
            continue

        if is_aligned(IS_aln1[0]) and is_aligned(IS_aln2[0]):
            continue
        elif is_aligned(genome_aln1[0]) and is_aligned(IS_aln2[0]):
            if not passes_genome_class_exclusions(class1):
                continue
            elif not passes_IS_class_exclusions(class2):
                continue

            flanking_reads_count = write_aln(genome_aln1, IS_aln2, class1, ref, outdir, flank_sams_out, flanking_reads_count)

        elif is_aligned(IS_aln1[0]) and is_aligned(genome_aln2[0]):
            if not passes_genome_class_exclusions(class2):
                continue
            elif not passes_IS_class_exclusions(class1):
                continue

            flanking_reads_count = write_aln(genome_aln2, IS_aln1, class2, ref, outdir, flank_sams_out, flanking_reads_count)

        else:
            continue

    logger.info("Total reads counted: %d" % total_read_count)
    logger.info("Total flanking reads meeting criteria: %d" % flanking_reads_count)

def check_matching_reads(genome_aln1, genome_aln2, IS_aln1, IS_aln2, class1, class2):
    if genome_aln1[0]['QNAME'] == genome_aln2[0]['QNAME'] == IS_aln1[0]['QNAME'] == IS_aln2[0]['QNAME'] == class1['HEADER'] == class2['HEADER']:
        pass
    else:
        raise IndexError("The reads and the classifications need to be in the same order.")

def is_unclassif_read(classif):
    if classif['TAXID'] == '0':
        return True
    return False


def is_aligned(alignment):
    if alignment['RNAME'] == '*':
        return False
    else:
        return True

def write_aln(gen_algnmnts, IS_algnmnts, classif, ref, outdir, sams_out, flank_count):
    refbase = os.path.basename(ref).split('.')[0]
    for gen_aln in gen_algnmnts:
        for IS_aln in IS_algnmnts:
            IS = IS_aln['RNAME']
            outfile = os.path.join(outdir, '%s_read_aligned_to_%s_and_%s.sam' %(classif['TAXID'], IS, refbase))
            if outfile in sams_out:
                outline = [val for key, val in gen_aln.items()]
                outline[0] = outline[0]+':TAXID-%s'%classif['TAXID']
                sams_out[outfile].write("\t".join(outline)+'\n')
                flank_count += 1
            else:
                sams_out[outfile] = open(outfile, 'w')
                outline = [val for key, val in gen_aln.items()]
                outline[0] = outline[0] + ':TAXID-%s' % classif['TAXID']
                sams_out[outfile].write("\t".join(outline) + '\n')
                flank_count += 1
    return flank_count


def append_complete_class_exclusions(exclude):
    global complete_class_exclusions
    complete_class_exclusions.append(exclude)

def append_genome_class_exclusions(exclude):
    global genome_class_exclusions
    genome_class_exclusions.append(exclude)

def append_IS_class_exclusions(exclude):
    global IS_class_exclusions
    IS_class_exclusions.append(exclude)

def passes_complete_class_exclusions(class1, class2):
    global complete_class_exclusions
    for exclusion in complete_class_exclusions:
        if class1[exclusion[0]] == exclusion[1] or class2[exclusion[0]] == exclusion[1]:
            return False
    return True

def passes_genome_class_exclusions(classif):
    global genome_class_exclusions
    for exclusion in genome_class_exclusions:
        if classif[exclusion[0]] == exclusion[1]:
            return False
    return True

def passes_IS_class_exclusions(classif):
    global IS_class_exclusions
    for exclusion in IS_class_exclusions:
        if classif[exclusion[0]] == exclusion[1]:
            return False
    return True
