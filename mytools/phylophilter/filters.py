import logging, sys
import IO, shared

class Filter:

    def __init__(self, fastq_reads, read_to_taxid, taxonomy_nodes, logger_in=None):
        assert type(fastq_reads) is str, "The provided fastq file must be a string to the file location."
        assert type(read_to_taxid) is str, "The provided read-to-taxon-id file must be a string to the " \
                                           "file location."
        assert type(taxonomy_nodes) is list, "The provided taxonomy nodes must be a list of file location(s)"

        self.logger = logger_in
        self.fastq_gen = IO.read_fastq_paired_ends_interleaved(open(fastq_reads, 'r'))
        self.read_to_taxid_gen = IO.reads_to_taxids(open(read_to_taxid, 'r'))
        self.taxonomy_nodes = shared.get_taxon_nodes(taxonomy_nodes, self.logger)
        self.taxonomy_names = None


    def filter_reads_linear(self, start_taxon, num_ancestral_nodes=0, stop_taxon=None, paired_end=True):
        hierarchy = shared.get_taxon_hierarchy(start_taxon, self.taxonomy_nodes)
        if self.logger: self.logger.info("Complete Ancestral Lineage: "+str(hierarchy))

        hierarchy = hierarchy[:num_ancestral_nodes]
        if self.logger: self.logger.info("Complete Ancestral Lineage: " + str(hierarchy))

        if paired_end:
            while True:
                try:
                    reads = self.fastq_gen.next()
                    read_class = self.read_to_taxid_gen.next()

                    if reads.getTitles() == read_class.getTitles():
                        "THEY MATCH, GREAT"
                        sys.exit()


                except ValueError:
                    break

        else:
            while True:
                try:
                    reads = self.fastq_gen.next()
                    read_class = self.read_to_taxid_gen.next()



                except ValueError:
                    break
