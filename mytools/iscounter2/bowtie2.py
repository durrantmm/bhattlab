"""
Wrapper script for bowtie2-align and bowtie2-build with version control
"""
import subprocess
from glob import glob
import os, sys

def build_all(directory, suffix="fasta"):
    fasta_files = glob(os.path.join(directory,"*.%s") % suffix)
    for fasta in fasta_files:
        if len(glob(os.path.join(directory,"%s.*" % fasta))) == 0:
            build('2.2.9', fasta)

def align_all(ref_directory, fastq_file, output_dir, threads=1, suffix="fasta"):
    fasta_files = glob(os.path.join(ref_directory,"*.%s" % suffix))
    for fasta in fasta_files:
        align('2.2.9', fasta, fastq_file, output_dir, threads=threads)


def build(version, fasta):
    """
    Construct bowtie2 indices (.bt2 files)
    :param version: Enforces bowtie2 version number (e.g., '2.2.1')
    :param fasta: Path to FASTA containing reference sequences
    :return:
    """
    try:
        subprocess.check_output(['bowtie2-build', '-h'])
    except OSError:
        raise RuntimeError('bowtie2-build not found; check if it is installed and in $PATH\n')

    stdout = subprocess.check_output(['bowtie2-build', '--version'])
    local_version = stdout.split('\n')[0].split()[-1]
    assert version == local_version, 'bowtie2-build version incompatibility %s != %s' % (version, local_version)
    subprocess.check_call(['bowtie2-build', '-q', '-f', fasta, fasta])


def align(version, refpath, fastq, output_dir, threads=1, flags=('--no-unal', '--local', '--quiet', '--all')):
    """
    Call bowtie2-align on paired read data
    :param version: Enforces bowtie2 version number
    :param refpath: Path to bowtie2 index files (.bt2)
    :param fastq: File.
    :param flags: A tuple of bowtie2 flags such as --local
    :return:
    """

    # check that we have access to bowtie2
    try:
        subprocess.check_output(['bowtie2', '-h'])
    except OSError:
        raise RuntimeError('bowtie2 not found; check if it is installed and in $PATH\n')

    # check that version is the expected version
    stdout = subprocess.check_output(['bowtie2', '--version'])
    local_version = stdout.split('\n')[0].split()[-1]
    assert version == local_version, 'bowtie2 version incompatibility %s != %s' % (version, local_version)

    # stream output from bowtie2
    bowtie_args = " ".join(['bowtie2', '-x', refpath, '-U', fastq, '-S %s/%s.sam' %
                            (output_dir, os.path.basename(refpath)), '-p', str(threads)] + list(flags))

    subprocess.call(bowtie_args, shell=True)
    return '%s/%s.sam' % (output_dir, os.path.basename(refpath))