import argparse
import sys
from collections import defaultdict
from Bio import SeqIO

# start here when the script is launched

def main(args):

    ref = get_reference(args['reference'])
    n_indices = get_n_indices(ref.seq)
    print ref.seq[n_indices[0][0]-10: n_indices[0][1]+10]

def get_reference(reference_loc):
    reference = {}
    with open(reference_loc) as refin:
        reference = SeqIO.to_dict(SeqIO.parse(refin, "fasta"))
    ref = reference[ reference.keys()[0]]
    return ref

def get_n_indices(ref_seq):
    index = 0
    n_indices = []
    contig_start = -1
    contig_end = -1
    for nuc in ref_seq:

        if nuc == 'N':
            if index == contig_end+1:
                contig_end += 1
            else:
                contig_start = index
                contig_end = index

        elif contig_end >= 0:
            n_indices.append((contig_start, contig_end))
            contig_start = -1
            contig_end = -1

        index+=1
    return n_indices




if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('-r', '--reference', required=True, help='FILL THIS OUT')
    parser.add_argument('-i', '--insertion', required=True, help='FILL THIS OUT')
    parser.add_argument('-n', '--number', required=False, default=1, help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)


    main(args)
