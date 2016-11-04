import sys

import IO
import shared
from collections import defaultdict


class Filter:

    def __init__(self, fastq_reads, read_to_taxid, taxonomy_nodes, logger_in=None):
        assert type(fastq_reads) is str, "The provided fastq file must be a string to the file location."
        assert type(read_to_taxid) is str, "The provided read-to-taxon-id file must be a string to the " \
                                           "file location."
        assert type(taxonomy_nodes) is list, "The provided taxonomy nodes must be a list of file location(s)"

        self.logger = logger_in

        self.fastq_paired_gen = IO.read_fastq_paired_ends_interleaved(open(fastq_reads, 'r'))
        self.fastq_non_paired_gen = IO.read_fastq_non_paired(open(fastq_reads, 'r'))

        self.read_to_taxid_paired_gen = IO.paired_reads_to_taxids(open(read_to_taxid, 'r'))
        self.read_to_taxid_non_paired_gen = IO.non_paired_reads_to_taxids(open(read_to_taxid, 'r'))

        self.taxonomy_nodes = shared.get_taxon_nodes(taxonomy_nodes, self.logger)
        self.taxonomy_names = None

    def filter_reads_ISCounter2(self, aligned_reads):

        if self.logger: self.logger.info("Loading the insertion sequence alignments...")
        IS_align_gen = IO.read_insertion_alignments(open(aligned_reads, 'r'))
        if self.logger: self.logger.info("Total aligned single reads: %s" % num_aligned)


        potential_transfers = 0
        intra_IS = 0
        unclassif_count = 0

        taxon_total_count = defaultdict(int)
        taxon_IS_count = defaultdict(lambda: defaultdict(int))


        total_read_count = 0
        total_classified_reads = 0

        saved_taxonomies = {}
        for reads, classes in zip(self.fastq_paired_gen, self.read_to_taxid_paired_gen):

            read1, read2 = reads.getTitles()
            class1, class2 = classes.getClassifs()

            # Check the reads and the classifications align
            #if [read1, read2] != classes.getTitles():
            #    if self.logger: self.logger.error("The reads do not match")
            #    raise IndexError("The reads and the classifications need to be in the same order.")

            total_read_count += 1
            if total_read_count % 100 == 0:
                if self.logger: self.logger.info("Reads sorted so far: %s" % total_read_count)

            # Discard it if EITHER READ is UNCLASSIFIED
            if class1 == '0' or class2 == '0':
                unclassif_count += 1

            # Check that read1 aligns to insertion sequence
            elif read1 in IS_aligned_dict.keys():

                # Check that read2 aligns to insertion sequence, send to intra_IS
                if read2 in IS_aligned_dict.keys():
                    #intra_IS.append(read1)
                    #intra_IS.append(read2)
                    intra_IS += 1

                # Otherwise, increment the read2 taxon_IS_count
                else:
                    taxon_total_count[class2] += 1
                    total_classified_reads += 1
                    for IS in IS_aligned_dict[read1]:
                        taxon_IS_count[class2][IS] += 1

            # Check that read2 aligns to insertion sequence
            elif read2 in IS_aligned_dict.keys():

                # Check that read1 aligns to insertion sequence, send to intra_IS
                if read1 in IS_aligned_dict.keys():
                    #intra_IS.append(read1)
                    #intra_IS.append(read2)
                    intra_IS += 1

                # Otherwise, increment the read1 taxon_IS_count
                else:
                    taxon_total_count[class1] += 1
                    total_classified_reads += 1
                    for IS in IS_aligned_dict[read2]:
                        taxon_IS_count[class1][IS] += 1

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

        if self.logger:
            self.logger.info("Total Read Count: %s" % total_read_count)
            self.logger.info("Total Unclassified: %s" % unclassif_count)
            self.logger.info("Total Classified and Counted: %s" % total_classified_reads)
            self.logger.info("Total potential transfers: %d" % (potential_transfers/2))
            self.logger.info("Total intra-IS read pairs: %d" % (intra_IS/2))

        return [dict(taxon_total_count), dict(taxon_IS_count), potential_transfers, intra_IS]


def truncate_at_bacteria(self, hierarchy, bacteria_taxon='2'):
        bacteria_index = 0
        for i in range(len(hierarchy)):
            if hierarchy[i] == bacteria_taxon:
                bacteria_index = i
        return hierarchy[:i+1]