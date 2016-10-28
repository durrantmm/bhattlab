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

    def filter_reads_linear(self, start_taxon, paired_end=True, num_ancestral_nodes=8, stop_taxon=None):
        hierarchy = shared.get_taxon_hierarchy_list(start_taxon, self.taxonomy_nodes)
        if self.logger: self.logger.info("Complete Ancestral Lineage:\n\t" + str(hierarchy))

        hierarchy = set(hierarchy[:num_ancestral_nodes + 1])

        if self.logger: self.logger.info("All ancestral nodes included in filter:\n\t" + str(hierarchy))

        if paired_end:
            if self.logger: self.logger.info("Performing paired end filtering...")
        else:
            if self.logger: self.logger.info("Performing single read filtering...")

        while True:

            try:
                # For paired ends
                if paired_end:

                    reads = self.fastq_paired_gen.next()
                    read_class = self.read_to_taxid_paired_gen.next()

                    if reads.getTitles() != read_class.getTitles():
                        if self.logger: self.logger.error("The reads do not match")
                        raise IndexError("The reads and the classifications need to be in the same order.")

                    # Now check that both reads are found within the ancestral line of the taxon.
                    if read_class.getClassifs()[0] in hierarchy and read_class.getClassifs()[1] in hierarchy:
                        yield reads.getReads()
                    else:
                        continue

                # For non-paired
                else:
                    sys.exit()
                    read = self.fastq_non_paired_gen.next()
                    read_class = self.read_to_taxid_non_paired_gen.next()
                    if read.getTitle() != read_class.getTitle():
                        self.logger.error("The read information does not match")
                        raise IndexError("The reads and the classifications need to be in the same order.")

                    if read_class.getClassif() in hierarchy:
                        yield read
                    else:
                        continue


            except ValueError:
                if self.logger: self.logger.debug("There was a ValueError in filter_reads_linear()")
                break


    def filter_reads_linear_ismapper(self, start_taxon, paired_end=True, num_ancestral_nodes=8, stop_taxon=None):

        hierarchy = shared.get_taxon_hierarchy_list(start_taxon, self.taxonomy_nodes)
        if self.logger: self.logger.info("Complete Ancestral Lineage:\n\t"+str(hierarchy))

        hierarchy = self.truncate_at_bacteria(hierarchy)
        if self.logger: self.logger.info("Truncated Ancestral Lineage:\n\t" + str(hierarchy))
        hierarchy = set(hierarchy)
        if self.logger: self.logger.info("All ancestral nodes included in filter:\n\t" + str(hierarchy))

        if paired_end:
            if self.logger: self.logger.info("Performing paired end filtering...")
        else:
            if self.logger: self.logger.info("Performing single read filtering...")

        while True:

            try:
                # For paired ends
                if paired_end:

                    reads = self.fastq_paired_gen.next()
                    read_class = self.read_to_taxid_paired_gen.next()

                    if reads.getTitles() != read_class.getTitles():
                        if self.logger: self.logger.error("The reads do not match")
                        raise IndexError("The reads and the classifications need to be in the same order.")

                    # First check that at least one of the reads is found at the level of the start taxon
                    if read_class.getClassifs()[0] == start_taxon or read_class.getClassifs()[1] == start_taxon:

                        # Now check that both reads are found within the ancestral line of the taxon.
                        if read_class.getClassifs()[0] in hierarchy and read_class.getClassifs()[1] in hierarchy:

                            yield reads.getReads()
                    else:
                        continue

                # For non-paired
                else:
                    sys.exit()
                    read = self.fastq_non_paired_gen.next()
                    read_class = self.read_to_taxid_non_paired_gen.next()
                    if read.getTitle() != read_class.getTitle():
                        self.logger.error("The read information does not match")
                        raise IndexError("The reads and the classifications need to be in the same order.")

                    if read_class.getClassif() in hierarchy:
                        yield read
                    else:
                        continue


            except ValueError:
                if self.logger: self.logger.debug("There was a ValueError in filter_reads_linear()")
                break


    def truncate_at_bacteria(self, hierarchy, bacteria_taxon='2'):
        bacteria_index = 0
        for i in range(len(hierarchy)):
            if hierarchy[i] == bacteria_taxon:
                bacteria_index = i
        return hierarchy[:i+1]