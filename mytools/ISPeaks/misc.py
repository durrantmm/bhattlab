import os

def makedir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return os.path.abspath(path)

def loop_counter(loop_count, total_read_count, logger, loop_count_out=1000000):
    loop_count += 1
    if loop_count == loop_count_out:
        logger.info("Total Reads Processed: %d" % total_read_count)
        loop_count = 0
    return loop_count