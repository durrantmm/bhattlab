import Bio
import sys

from Bio import SeqIO
handle = open(sys.argv[1], 'rU')
for record in SeqIO.parse(handle, "fasta"):
    with open(record.id+".fasta","w") as outfile:
        SeqIO.write(record, outfile, "fasta")

handle.close()