import argparse, logging
import sys, os
import pprint, ast
from datetime import datetime
from phylophilter import filters, IO, shared
import bowtie2
from glob import glob
from itertools import izip

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s:\t%(message)s")
    logger = logging.getLogger()

    out_prefix = ''
    if not args['out_prefix']:
        args['out_prefix'] = create_out_prefix(args)

    if not args['classifications']:
        args['classifications'] = args['fastq']+'.results.tsv'


    IS_sam = IO.read_insertion_alignments(open(args['insertion_sam']), args['insertion_sam'])
    fastq = IO.read_fastq_paired_ends_interleaved(open(args['fastq']))
    classifs = IO.paired_reads_to_taxids(open(args['classifications']))

    filtered_fastq = ''
    with open(args['out_prefix']+'.fq', 'w') as fq_out:
        fq_out.write("TEST1\n")
        fq_out.write("TEST2\n")

        filtered_fastq = filter_flanks_to_fastq(IS_sam, fastq, classifs, args['taxon'], args['insertion_sequence'],
                                                fq_out, logger)

    logger.info("Flanking reads saved to output fastq: %s" % filtered_fastq)

    logger.info("Building the given genome file...")
    bowtie2.build('2.2.9', args['genome'])
    genome_aligned_sam_loc = bowtie2.align_genome('2.2.9', args['genome'], filtered_fastq, args['out_prefix'])
    print genome_aligned_sam_loc

def create_out_prefix(args):
    out_prefix = os.path.dirname(os.path.abspath(args['insertion_sam']))+'/'
    out_prefix = out_prefix + os.path.basename(args['fastq']).split('.')[0]

    out_prefix = out_prefix + "_taxa_%s_" % "_".join(list(args['taxon']))
    out_prefix = out_prefix + "reads_flanking_%s_" % args['insertion_sequence']
    out_prefix = out_prefix + "aligned_to_%s" % os.path.basename(args['genome']).split('.')[0]

    return out_prefix


def filter_flanks_to_fastq(IS_sam, fastq, classifs, taxa, insertion, out_fastq, logger=None):
    taxa = set(list(taxa))
    aligned_read, aligned_IS = IS_sam.next()
    loop_count = 0

    total_read_count = 0
    flanking_reads_count = 0

    out_fastq.write("Test3\n")

    if logger: logger.info("Beginning read filtering...")
    for reads, classes in izip(fastq, classifs):
        total_read_count += 1
        loop_count = shared.loop_counter(loop_count, total_read_count, logger)

        read1, read2 = reads.getTitles()
        class1, class2 = classes.getClassifs()
        # print read1[-10:], read2[-10:], self.aligned_read[-10:]

        # Check the reads and the classifications align
        if [read1, read2] != classes.getTitles():
            if logger: logger.error("The reads do not match")
            raise IndexError("The reads and the classifications need to be in the same order.")

        # Discard it if EITHER READ is UNCLASSIFIED
        if class1 not in taxa and class2 not in taxa:
            if read1 == aligned_read:
                aligned_read, aligned_IS = IS_sam.next()
            if read2 == aligned_read:
                aligned_read, aligned_IS = IS_sam.next()

        # Check that read1 aligns to insertion sequence
        elif read1 == aligned_read:
            tmp_aligned_read, tmp_aligned_IS = IS_sam.next()

            # Check that read2 aligns to insertion sequence, send to intra_IS
            if read2 == tmp_aligned_read:
                aligned_read, aligned_IS = IS_sam.next()
                continue

            # Otherwise, increment the read2 taxon_IS_count
            else:
                for IS in aligned_IS:
                    if IS == insertion and class2 in taxa:
                        logger.info("Flanking read classified as %s: %s" % (class2, read2))
                        outread = reads.getReads()[1]
                        outread[0], outread[-1] = ("%s:TAXON-%s" % (outread[0], class2), outread[-1].strip())
                        print outread
                        out_fastq.write("\n".join(outread) + "\n")
                        flanking_reads_count += 1

                aligned_read, aligned_IS = tmp_aligned_read, tmp_aligned_IS

        # Check that read2 aligns to insertion sequence
        elif read2 == aligned_read:

            for IS in aligned_IS:
                if IS == insertion and class1 in taxa:
                    logger.info("Flanking read classified as %s: %s" % (class1, read1))
                    outread = reads.getReads()[0]
                    outread[0], outread[-1] = ("%s:TAXON-%s" % (outread[0], class1), outread[-1].strip())
                    print outread
                    print out_fastq.write("\n".join(outread)+"\n")
                    flanking_reads_count += 1


            aligned_read, aligned_IS = IS_sam.next()

        # If they are the same class, and neither maps to IS.
        else:
            continue

    logger.info("Total reads counted: %d" % total_read_count)
    logger.info("Total flanking reads meeting criteria: %d" % flanking_reads_count)
    return out_fastq.name



if __name__ == "__main__":

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    output_dir = os.path.join(current_dir, "output2")
    timestamp = ":".join([str(datetime.now().time()), str(datetime.now().date())])

    # setup the option parser
    parser = argparse.ArgumentParser(description='')

    # add universal arguments, arguments to be specified regardless of the type of arguments that follow.
    parser.add_argument('-fq', '--fastq', required=True,
                        help='The original fastq file of interest')

    parser.add_argument('-is', '--insertion_sequence', required=True, type=str,
                        help='The insertion sequence in the results that are to be analyzed')

    parser.add_argument('-sam', '--insertion_sam', required=True,
                        help='The insertion-aligned sam file')

    parser.add_argument('-c', '--classifications', required=False,
                        help='The output prefix to use')

    parser.add_argument('-t', '--taxon', required=True, nargs='*',
                        help='The taxon of interest to analyze')

    parser.add_argument('-g', '--genome', required=True,
                        help='A genome, or other fasta file of interest, to align the flanks to.')

    parser.add_argument('-o', '--out_prefix', required=False,
                        help='The output prefix to use')

    args = parser.parse_args()
    args = vars(args)

    main(args)

