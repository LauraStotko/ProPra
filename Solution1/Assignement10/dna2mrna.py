#!/usr/bin/python3
import argparse

def read_fasta(fasta_file):

    sequences = {}
    current_id = None
    current = ''
    # go trough every line of the file and save the sequence_id with the corresponding sequence in a dictionary
    for l in fasta_file:
        # returns the same string without spaces
        l = l.strip()
        # first line of new sequence, contains the sequence_id
        if l.startswith('>'):
            if current_id:
                sequences[current_id] = current
                current=''
            #save new id
            current_id = l.strip()[1:]
        else:
            # add line of sequence to the current sequence
            current += l
    if current_id:
        sequences[current_id] = current
    return sequences

def dna2mrna(infile):
    sequences = read_fasta(infile)
    mrna_sequences = {}
    for sequence_id, sequence in sequences.items():
        mrna = dna_to_mrna(sequence)
        # save in new dictionary
        mrna_sequences[sequence_id] = mrna
    return mrna_sequences


def dna_to_mrna(dna_sequence):
    mrna_sequence = ""
    # replace T with U for mrna
    for base in dna_sequence:
        if base == 'T':
            mrna_sequence += 'U'
        else:
            mrna_sequence += base
    return mrna_sequence

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Translate DNA to mRNA")
    pars.add_argument("--fasta", type = argparse.FileType('r'), required=True)
    args = pars.parse_args()

    mrna_sequences = dna2mrna(args.fasta)

    for sequence_id, sequence in mrna_sequences.items():
        print(f'>{sequence_id}')
        sequence = sequence.rstrip('\n')
        print(sequence)


