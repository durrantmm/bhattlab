import os, sys
from os.path import basename
from pprint import pprint
from glob import glob
from collections import defaultdict

def count_lines(file_in, skip_header=False):
    count = 0
    for line in file_in: count += 1

    if skip_header: return count-1
    else: return count

def loop_counter(loop_count, total_read_count, logger, loop_count_out=1000000):
    loop_count += 1
    if loop_count == loop_count_out:
        logger.info("Total Reads Processed: %d" % total_read_count)
        loop_count = 0
    return loop_count

def calc_threads_start_stop(num_reads, threads):
    read_pos = 1
    reads_per_thread = num_reads / threads
    remainder = num_reads-(threads*reads_per_thread)

    start_stop = []
    for i in range(threads):
        if i != threads - 1:
            start_stop.append((read_pos, read_pos+reads_per_thread-1))
        else:
            start_stop.append((read_pos, read_pos + reads_per_thread - 1 + remainder))
        read_pos += reads_per_thread

    return start_stop

def calc_threads_start_stop(num_reads, threads):
    read_pos = 1
    reads_per_thread = num_reads / threads
    remainder = num_reads-(threads*reads_per_thread)

    start_stop = []
    for i in range(threads):
        if i != threads - 1:
            start_stop.append((read_pos, read_pos+reads_per_thread-1))
        else:
            start_stop.append((read_pos, read_pos + reads_per_thread - 1 + remainder))
        read_pos += reads_per_thread

    return start_stop

def consolidate_sams(dir, delim):
    sams = glob(dir+'/*')
    sams_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    cons_groups = set()
    for sam in sams:
        genome, taxon, insert, proc = basename(sam).split(delim)
        readcount = count_lines(open(sam), skip_header = False)
        sams_dict[genome][taxon][insert] += readcount
        cons_groups.add(os.path.join(dir, delim.join(basename(sam).split(delim)[:-1])+delim))

    for path in cons_groups:
        group = glob(path+'*')
        cat_delete(path.strip(delim), group)

def cat_delete(outpath, group):

    with open(outpath+'.sam','w') as out:

        for path in group:
            with open(path) as infile:
                for line in infile:
                    out.write(line)
            os.remove(path)


