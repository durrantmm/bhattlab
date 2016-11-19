import os
from log import Log

class SingleState:
    def __init__(self, args):
        self.which = 'single'

        self.paths = Paths(fastq_files = args['fastqs'],
                           fastq_to_IS_algnmnts=['fastq1_to_IS.sam', 'fastq2_to_IS.sam'],
                           class_files = args['classifications'],
                           insertion_fasta=args['insertion_fasta'],
                           reference_genomes=args['reference_genomes'],
                           outdir=args['output_dir'])

        self.settings = Settings(args['complete_class_exclusions'],
                                 args['genome_class_exclusions'],
                                 args['insertion_class_exclusions'],
                                 args['threads'],
                                 args['num_reads'])

        self.logger = Log(self.paths.out_dir)

    def print_state(self):
        print "FASTQ FILES:", self.paths.fastq_files
        print "CLASSIFICATION FILES:", self.paths.class_files
        print "INSERTION FASTA:", self.paths.insertion_fasta
        print "OUTPUT DIRECTORY:", self.paths.out_dir
        print "SAMS DIR:", self.paths.sams_dir
        print "FULL SAMS DIR:", self.paths.full_sams_dir
        print "TAXON SORTED SAMS DIR:", self.paths.taxon_sorted_sams_dir
        print
        print "COMPLETE CLASS EXCLUSIONS:", self.settings.complete_class_exclusions
        print "GENOME CLASS EXCLUSIONS:", self.settings.genome_class_exclusions
        print "INSERTION CLASS EXCLUSIONS:", self.settings.insertion_class_exclusions
        print "REFERENCE GENOMES:", self.paths.reference_genomes

class Paths:
    def __init__(self, fastq_files, fastq_to_IS_algnmnts, class_files, insertion_fasta, reference_genomes, outdir):

        # Directories
        self.out_dir = self.makedir(outdir)
        self.sams_dir = self.makedir(os.path.join(outdir, 'sams'))
        self.full_sams_dir = self.makedir(os.path.join(outdir, 'sams', 'full_sams'))
        self.taxon_sorted_sams_dir = self.makedir(os.path.join(outdir, 'sams', 'taxon_sorted_sams_dir'))

        # Files
        self.fastq_files = fastq_files
        self.fastq_to_IS_algnmnts = [os.path.join(self.full_sams_dir, os.path.basename(path)) for path in fastq_to_IS_algnmnts]
        self.class_files = class_files
        self.insertion_fasta = insertion_fasta
        self.reference_genomes = reference_genomes
        self.fastq_to_genome_algnmnts = None

    def makedir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)
        return os.path.abspath(path)

class Settings:
    def __init__(self, complete_class_exclusions, genome_class_exclusions, insertion_class_exclusions, threads, num_reads):
        self.complete_class_exclusions = complete_class_exclusions
        self.genome_class_exclusions = genome_class_exclusions
        self.insertion_class_exclusions = insertion_class_exclusions
        self.threads = threads
        self.num_reads = num_reads