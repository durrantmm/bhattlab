import argparse
from os.path import join


def main(args):
    commands = parse_commands(args['commands'])


    for com in commands:
        outstr = """#!/bin/sh
#
# set the name of the job
#$ -N %s
#
# set the maximum memory usage (per slot)
#$ -l h_vmem=%s
#
# set the maximum run time
#$ -l h_rt=%s
#
# send mail when job ends or aborts
#$ -m bea
#
# specify an email address
#$ -M mdurrant@stanford.edu
#
# specify the account name
#$ -A bhatt
#
# check for errors in the job submission options
#$ -w w
#
# output logfile
#$ -o log_%s
#
#$ -cwd
%s""" % (com['NAME'], args['memory'], args['time'], com['NAME'], com['COMMAND'])
        with open(join(args['out_dir'], "submit_%s.sh" % com['NAME']), 'w') as out:
            out.write(outstr)

def parse_commands(commands_path):
    commands = []
    with open(commands_path, 'r') as infile:
        header = [i.upper() for i in infile.readline().strip().split('\t')]
        for line in infile:
            line = {header[i]: line.strip().split('\t')[i] for i in range(len(line.strip().split('\t')))}
            commands.append(line)
    return commands


if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('-c','--commands', required = True,
                        help='FILL THIS OUT')
    parser.add_argument('-t', '--time', required=True,
                        help='FILL THIS OUT')
    parser.add_argument('-m', '--memory', required=True,
                        help='FILL THIS OUT')
    parser.add_argument('-e', '--email', required=True,
                        help='FILL THIS OUT')
    parser.add_argument('-o', '--out-dir', required=True,
                        help='FILL THIS OUT')


    args = parser.parse_args()
    args = vars(args)

    print args
    main(args)