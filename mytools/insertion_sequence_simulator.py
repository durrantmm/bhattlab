import argparse
import sys
from collections import defaultdict
from Bio import SeqIO
from random import randrange

# start here when the script is launched

def main(args):

    ref = get_reference(args['reference'])
    print("Reference sequence length: %s" % len(ref.seq))

    insertion = get_insertion(args['insertion'])
    n_indices = get_n_indices(ref.seq)

    insertion_sites = []

    while len(insertion_sites) < int(args['number']):
        insertion_site = 0
        while not valid_insertion_site(insertion_site, n_indices, len(ref.seq), insertion_sites):
            insertion_site = randrange(0, len(ref.seq)+1)
        insertion_sites.append(insertion_site)

    insertion_sites.sort()
    print insertion_sites
    new_seq = ""
    start_site = 0
    for site in insertion_sites:
        print "Inserting sequence at position %d" % site
        new_seq = new_seq + ref.seq[start_site:site] + insertion.seq
        start_site = site
    new_seq = new_seq + ref.seq[start_site:]
    ref.seq = new_seq

    print("New reference sequence length: %d" % len(ref.seq))

    with open(args['output'],'w') as outfile:
        SeqIO.write(ref, outfile, "fasta")





def valid_insertion_site(insertion_site, n_indices, ref_len, insertion_sites):
    if insertion_site < 500 or insertion_site > ref_len-500:
        return False

    for site in insertion_sites:
        if insertion_site < site+2000 and insertion_site > site-2000:
            return False

    for nrange in n_indices:
        if insertion_site > nrange[0]-500 and insertion_site < nrange[1]:
            return False
        elif insertion_site < nrange[1]+500 and insertion_site > nrange[0]:
            return False
    return True


def get_reference(reference_loc):
    reference = {}
    with open(reference_loc) as refin:
        reference = SeqIO.to_dict(SeqIO.parse(refin, "fasta"))
    ref = reference[ reference.keys()[0]]
    return ref


def get_insertion(insertion_loc):
    insertion = {}
    with open(insertion_loc) as insert_in:
        insertion = SeqIO.to_dict(SeqIO.parse(insert_in, "fasta"))
    insertion = insertion[ insertion.keys()[0]]
    return insertion

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
    parser.add_argument('-o', '--output', required=False, default="inserted_seq.fasta", help='FILL THIS OUT')
    parser.add_argument('-n', '--number', required=False, default=1, help='FILL THIS OUT')

    args = parser.parse_args()
    args = vars(args)


    main(args)
