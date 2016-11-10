import argparse, logging
import sys, os
import pprint, ast
from datetime import datetime
from phylophilter import filters, IO
import bowtie2
from glob import glob

def main(args):
    logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s:\t%(message)s")
    logger = logging.getLogger()

    out_prefix = ''
    if not args['out_prefix']:
        out_prefix = create_out_prefix(args)
    else:
        out_prefix = args['out_prefix']


    IS_sam = IO.read_insertion_alignments(open(args['insertion_sam']), args['insertion_sam'])
    fastq = IO.read_fastq_paired_ends_interleaved(open(args['fastq']))
    classifs = IO.paired_reads_to_taxids(args['classifications'])

    filtered_fastq = filter_flanks(IS_sam, fastq, classifs, args['taxon'], out_prefix+'.fq')

def create_out_prefix(args):
    out_prefix = os.path.dirname(os.path.abspath(args['insertion_sam']))+'/'
    out_prefix = out_prefix + os.path.basename(args['fastq']).split('.')[0]

    out_prefix = out_prefix + "_taxa_%s_" % "_".join(list(args['taxon']))
    out_prefix = out_prefix + "reads_flanking_%s_" % args['insertion_sequence']
    out_prefix = out_prefix + "aligned_to_%s" % os.path.basename(args['genome']).split('.')[0]

    return out_prefix


def filter_flanks(IS_sam, fastq, classifs, taxa, out_folder):
    print IS_sam, fastq, calssifs, taxa, out_folder
    sys.exit()
    saved_taxonomies = {}
    self.aligned_read, self.aligned_IS = self.IS_align_gen.next()
    loop_count = 0

    if self.logger: self.logger.info("Beginning read classification and read sorting...")
    for reads, classes in izip(self.fastq_paired_gen, self.read_to_taxid_paired_gen):
        total_read_count += 1
        loop_count = shared.loop_counter(loop_count, total_read_count, self.logger)

        read1, read2 = reads.getTitles()
        class1, class2 = classes.getClassifs()
        # print read1[-10:], read2[-10:], self.aligned_read[-10:]

        # Check the reads and the classifications align
        if [read1, read2] != classes.getTitles():
            if self.logger: self.logger.error("The reads do not match")
            raise IndexError("The reads and the classifications need to be in the same order.")

        # Discard it if EITHER READ is UNCLASSIFIED
        if class1 == '0' or class2 == '0':
            if read1 == self.aligned_read:
                self.aligned_read, self.aligned_IS = self.IS_align_gen.next()
            if read2 == self.aligned_read:
                self.aligned_read, self.aligned_IS = self.IS_align_gen.next()
            unclassif_count += 1

        # Check that read1 aligns to insertion sequence
        elif read1 == self.aligned_read:
            tmp_aligned_read, tmp_aligned_IS = self.IS_align_gen.next()

            # Check that read2 aligns to insertion sequence, send to intra_IS
            if read2 == tmp_aligned_read:
                self.aligned_read, self.aligned_IS = self.IS_align_gen.next()
                intra_IS += 1

            # Otherwise, increment the read2 taxon_IS_count
            else:
                taxon_total_count[class2] += 1
                total_classified_reads += 1
                for IS in self.aligned_IS:
                    taxon_IS_count[class2][IS] += 1
                self.aligned_read, self.aligned_IS = tmp_aligned_read, tmp_aligned_IS

        # Check that read2 aligns to insertion sequence
        elif read2 == self.aligned_read:
            taxon_total_count[class1] += 1
            total_classified_reads += 1
            for IS in self.aligned_IS:
                taxon_IS_count[class1][IS] += 1
            self.aligned_read, self.aligned_IS = self.IS_align_gen.next()

        # If they are the same class, and neither maps to IS.
        elif class1 == class2:
            total_classified_reads += 1
            taxon_total_count[class1] += 1

        # If they are different class, check for relatedness.
        else:
            try:
                taxonomy1 = saved_taxonomies[class1]
            except KeyError:
                taxonomy1 = shared.get_taxon_hierarchy_set(class1, self.taxonomy_nodes)
                saved_taxonomies[class1] = taxonomy1

            try:
                taxonomy2 = saved_taxonomies[class2]
            except KeyError:
                taxonomy2 = shared.get_taxon_hierarchy_set(class2, self.taxonomy_nodes)
                saved_taxonomies[class2] = taxonomy2

            if shared.is_parent_child(class1, taxonomy1, class2, taxonomy2):
                if shared.which_parent_child(class1, taxonomy1, class2, taxonomy2) == 0:
                    total_classified_reads += 1
                    taxon_total_count[class1] += 1

                else:
                    total_classified_reads += 1
                    taxon_total_count[class2] += 1
            else:
                # potential_transfers.append("|".join([read1, class1]))
                # potential_transfers.append("|".join([read2, class2]))
                potential_transfers += 1

        if total_read_count != unclassif_count + total_classified_reads + potential_transfers + intra_IS:
            raise ArithmeticError("Something is not adding up correctly...")
            print reads
            print classes
            print self.aligned_IS
            sys.exit()

    return [dict(taxon_total_count), dict(taxon_IS_count), potential_transfers, intra_IS]



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

