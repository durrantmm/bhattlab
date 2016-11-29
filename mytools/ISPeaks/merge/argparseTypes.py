import argparse
import os, sys

ref_basenames = set()

def ispeaks_directory(path):

    try:
        if not os.path.isdir(path): raise TypeError()
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Please give paths to valid fastq files.')

def output_folder(path):
    try:
        if os.path.isdir(path):
            raise TypeError()
        return os.path.abspath(path)
    except:
        raise argparse.ArgumentTypeError('Output folder cannot already exist')

