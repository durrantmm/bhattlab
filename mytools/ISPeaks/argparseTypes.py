import os, argparse, re, sys
from glob import glob

def genome(path):
    try:
        if not os.path.isfile(path): raise TypeError("Genome fasta is not a file.")
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError("Genomes must be entered as \"<reference-fasta1> <reference-fasta2>\"")

def insertion_fasta(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Please give a path to a valid fasta file.')


def fastq_file(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid fastq files.')


def class_file(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        print re.match('[^\w\d]', open(path).readline())

        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid classification files. Make sure that it contains'
                                         ' an alphanumeric characters and white space delimiters only.')


def output_folder(path):
    try:
        if os.path.isdir(path):
            if len(glob(path+'/*')) > 0:
                raise TypeError()
        return os.path.abspath(path)
    except:
        ##### TEMPORARY TO MAKE THINGS FASTER, DELETE THIS NEXT LINE LATER #####
        return path
        raise argparse.ArgumentTypeError('Output folder must be empty or non-existent.')


def taxon_nodes(path):
    try:
        if not os.path.isfile(path): raise TypeError()
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid taxonomy node files.')

