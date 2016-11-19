import os
from pprint import pprint

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



