import os, sys
from siteFinder import SiteFinder

def action(args, logger):

    bam = args['bam_file']
    peaks_path = args['peak_ranges']

    sitefinder = SiteFinder(bam, peaks_path, logger)
    sitefinder.find_sites()