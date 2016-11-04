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
        IS_aligned_dict = IO.get_insertion_alignments(aligned_reads)


        potential_transfers = set()
        intra_IS = set()
        taxon_total_count = defaultdict(int)
        taxon_IS_count = defaultdict(lambda: defaultdict(int))
        unclassif_count = 0
        for reads, classes in zip(self.fastq_paired_gen, self.read_to_taxid_paired_gen):

            if classes.getClassifs()[0] == '0' or classes.getClassifs[1] == '0':
                unclassif_count += 1
            elif reads.getTitles()[0] in IS_aligned_dict.keys():
                if reads.getTitles()[1] in IS_aligned_dict.keys():
                    intra_IS.add(reads.getTitles()[0]+ "|" + "|".join(list(IS_aligned_dict[reads.getTitles[0]])))
                    intra_IS.add(reads.getTitles()[1] + "|" + "|".join(list(IS_aligned_dict[reads.getTitles[1]])))
                else:
                    taxon_total_count[classes.getClassifs()[1]] += 1

            elif reads.getTitles()[1] in IS_aligned_dict.keys():
                if reads.getTitles()[0] in IS_aligned_dict.keys():
                    intra_IS.add(reads.getTitles()[0]+ "|" + "|".join(list(IS_aligned_dict[reads.getTitles[0]])))
                    intra_IS.add(reads.getTitles()[1] + "|" + "|".join(list(IS_aligned_dict[reads.getTitles[1]])))
                else:
                    taxon_total_count[classes.getClassifs()[0]] += 1

            elif classes.getClassifs()[0] == classes.getClassifs()[1]:
                taxon_total_count[classes.getClassifs()[0]] += 1

            else:
                taxonomy1 = shared.get_taxon_hierarchy_list(classes.getClassifs()[0], self.taxonomy_nodes)
                taxonomy2 = shared.get_taxon_hierarchy_list(classes.getClassifs()[1], self.taxonomy_nodes)
                print taxonomy1
                print taxonomy2
                sys.exit()



def truncate_at_bacteria(self, hierarchy, bacteria_taxon='2'):
        bacteria_index = 0
        for i in range(len(hierarchy)):
            if hierarchy[i] == bacteria_taxon:
                bacteria_index = i
        return hierarchy[:i+1]