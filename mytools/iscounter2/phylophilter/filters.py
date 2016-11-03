import sys

import IO
import shared


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

    def filter_reads_linear_ISCounter2(self, ):

        hierarchy = shared.get_taxon_hierarchy_list(start_taxon, self.taxonomy_nodes)


        if self.logger: self.logger.info("Performing paired end filtering to only include paired reads where at "
                                         "least one of the reads maps to the designated taxon...")

        while True:

            try:
                reads = self.fastq_paired_gen.next()
                read_class = self.read_to_taxid_paired_gen.next()

                if reads.getTitles() != read_class.getTitles():
                    if self.logger: self.logger.error("The reads do not match")
                    raise IndexError("The reads and the classifications need to be in the same order.")

                # Don't count read pairs where at least one is unclassified.
                if read_class.getClassifs()[0] == '0' or read_class.getClassifs()[1] == '0':
                    continue

                # Nowcheck that at least one of the reads is found at the level of the start taxon
                if read_class.getClassifs()[0] == start_taxon or read_class.getClassifs()[1] == start_taxon:
                    yield reads.getReads()

                else:
                    continue

                # For non-paired


            except ValueError:
                if self.logger: self.logger.debug("There was a ValueError in filter_reads_linear()")
                break

    def truncate_at_bacteria(self, hierarchy, bacteria_taxon='2'):
        bacteria_index = 0
        for i in range(len(hierarchy)):
            if hierarchy[i] == bacteria_taxon:
                bacteria_index = i
        return hierarchy[:i+1]