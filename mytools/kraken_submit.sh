#!/bin/sh
#
# set the name of the job
#$ -N kraken
#
# set the maximum memory usage (per slot)
#$ -l h_vmem=300G
#
# set the maximum run time
#$ -l h_rt=48:00:00
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
#$ -o kraken_submit_logfile
#
#$ -cwd

echo "kraken --db /srv/gsfs0/projects/bhatt/data/program_indices/kraken/kraken_custom --preload $1"
