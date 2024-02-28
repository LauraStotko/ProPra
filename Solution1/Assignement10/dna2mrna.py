#!/usr/bin/python3
import argparse
import sys

def read_fasta(fasta_file):

    sequences = {}
    current_id = None
    current = ''
    for l in fasta_file:
        l = l.strip()
        if l.startswith('>'):
            if current_id:
                sequences[current_id] = current
                current=''
            #neu anfangen
            current_id = l.strip()[1:]
        else:
            current += l
    if current_id:
        sequences[current_id] = current
    return sequences

def dna2mrna(infile):
    sequences = read_fasta(infile)
    mrna_sequences = {}
    for sequence_id, sequence in sequences.items():
        mrna = dna_to_mrna(sequence)
        mrna_sequences[sequence_id] = mrna
    return mrna_sequences


def dna_to_mrna(dna_sequence):
    mrna_sequence = ""
    for base in dna_sequence:
        if base == 'A':
            mrna_sequence += 'U'
        elif base == 'T':
            mrna_sequence += 'A'
        elif base == 'C':
            mrna_sequence += 'G'
        elif base == 'G':
            mrna_sequence += 'C'
    return mrna_sequence

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Translate DNA to mRNA")
    pars.add_argument("--fasta", type = str)
    args = pars.parse_args()

    if args.fasta:
        with open(args.fasta, 'r') as fasta_file:
            mrna_sequences = dna2mrna(fasta_file)
    else:
        mrna_sequences = dna2mrna(sys.stdin)

    for sequence_id, sequence in mrna_sequences.items():
        print(f'>{sequence_id}')
        sequence = sequence.rstrip('\n')
        print(sequence)


