import logging
import IO, shared

class Filter:

    def __init__(self, fastq_reads, read_to_taxid, taxon_nodes, logger_in=None):
        self.fastq_gen = IO.read_fastq_paired_ends_interleaved(open(fastq_reads, 'r'))
        self.read_to_taxid_gen = IO.reads_to_taxids(open(read_to_taxid, 'r'))
        self.logger = logger_in

    def filter_reads(self, taxon_id):
        while True:
            yield self.fastq_gen.next(), self.read_to_taxid_gen.next()

