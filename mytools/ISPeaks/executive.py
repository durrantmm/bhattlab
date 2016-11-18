import os
import bowtie2, phylosorter


def exec_single(args, logger):
    logger.info("Aligning the FASTQ files to the insertion sequences...")
    fastq1_path, fastq2_path = args['fastqs'][0], args['fastqs'][1]
    insertion_path = args['insertion_fasta']
    outdir = args['output_dir']
    threads = args['threads']

    logger.info("Building the insertion fasta file for alignment...")
    bowtie2.build('2.2.9', insertion_path, logger)

    logger.info("Aligning the forward reads in %s to the file %s" % (fastq1_path, insertion_path))
    outsam_fq1 = bowtie2.align_fastq_to_insertions('2.2.9', insertion_path, fastq1_path, outdir,
                                                   'fastq1_to_IS.sam', threads)
    logger.info("Output saved to %s" % outsam_fq1)

    logger.info("Aligning the reverse reads in %s to the file %s" % (fastq2_path, insertion_path))
    outsam_fq2 = bowtie2.align_fastq_to_insertions('2.2.9', insertion_path, fastq2_path, outdir,
                                                   'fastq2_to_IS.sam', threads)
    logger.info("Output saved to %s" % outsam_fq2)

    logger.info("Beginning alignment to all specified reference files...")
    refs = args['reference_genomes_single']
    ref_sams = align_to_references(fastq1_path, fastq2_path, refs, outdir, threads, logger)

    logger.info("Creating taxon-to-insertion sam files containing all insertion-flanking-reads...")
    nodes, class1, class2 = args['taxon_nodes'], args['classifications'][0], args['classifications'][1]
    phylosorter.sort_flanking_reads(outsam_fq1, outsam_fq2, class1, class2, ref_sams, outdir, logger)

    logger.info("Analysis Complete :)")


def align_to_references(fastq1, fastq2, references, outdir, threads, logger=None):
    ref_sams = {}
    for ref in references:
        refpath, taxon = ref, references[ref]
        suffix = os.path.basename(refpath).split('.')[0]

        if logger: logger.info("Building the genome fasta file for the file %s..." % refpath)
        bowtie2.build('2.2.9', refpath, logger)

        if logger: logger.info("Aligning the forward reads in %s to the genome found at %s which "
                               "represents the taxon %d" %(fastq1, refpath, taxon))
        outsam1 = bowtie2.align_to_genome('2.2.9', refpath, fastq1, outdir, 'fastq1_to_%d_genome_%s.sam' %
                                          (taxon, suffix), threads)

        if logger: logger.info("Aligning the reverse reads in %s to the genome found at %s which "
                               "represents the taxon %d" % (fastq2, refpath, taxon))
        outsam2 = bowtie2.align_to_genome('2.2.9', refpath, fastq2, outdir, 'fastq2_to_%d_genome_%s.sam' %
                                          (taxon, suffix), threads)

        ref_sams[refpath] = (outsam1, outsam2)
    return ref_sams

