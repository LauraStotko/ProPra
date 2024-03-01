#!/usr/bin/python3
import argparse
import re

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
                current = ''
            #save new id
            current_id = l.strip()[1:]
        else:
            #add line of sequence to the current sequence
            current += l
    if current_id:
        sequences[current_id] = current
    return sequences


def find_orfs(sequence):
    orf_sequences = []
    stop_codons = ["TAA", "TAG", "TGA"]
    start_codon = "ATG"
    i = 0

    while i < len(sequence):
        orf_sequence = ''
        current_codon = sequence[i:i+3]
        if current_codon != start_codon:
            i = i + 3
            continue
        orf_sequence += current_codon
        # da fange ich die Suche nach Stopp Codon an
        j = i+3
        while j < len(sequence):
            current_codon = sequence[j:j+3]
            orf_sequence += current_codon
            if current_codon in stop_codons:
                orf_sequences.append(orf_sequence)
                i = j+3
                break
            j += 3
            i = j

    return orf_sequences
def complement(sequence):
    result_sequence = ''
    for base in sequence:
        if base == 'A':
            result_sequence += 'T'
        elif base == 'T':
            result_sequence += 'A'
        elif base == 'C':
            result_sequence += 'G'
        elif base == 'G':
            result_sequence += 'C'
    return result_sequence[::-1]


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Find ORFs")
    pars.add_argument("--fasta", type=argparse.FileType('r'), required=True)
    pars.add_argument("--output", help= "path to output file", required=False)
    # add other arguments
    args = pars.parse_args()

    sequences = read_fasta(args.fasta)
    orf_sequences = {}

    for sequence_id, sequence in sequences.items():
        orf_sequences[sequence_id] = []
        orf_sequences[sequence_id] += find_orfs(sequence)
        orf_sequences[sequence_id] += find_orfs(sequence[1:])
        orf_sequences[sequence_id] += find_orfs(sequence[2:])

        revers_sequence = complement(sequence)
        orf_sequences[sequence_id] += find_orfs(revers_sequence)
        orf_sequences[sequence_id] += find_orfs(revers_sequence[1:])
        orf_sequences[sequence_id] += find_orfs(revers_sequence[2:])


    if args.output:
        path = f"{args.output}/{args.fasta.name}"
        with open(path, 'w') as f:
            for sequence_id, sequence in orf_sequences.items():
                counter = 0
                for sequence in sequences:
                    f.write(f">{sequence_id}_{counter}\n{sequence}")
                    counter += 1
            f.close()
    else:
        # print sequences on commmand line
        for sequence_id, sequences in orf_sequences.items():
            counter = 0
            for sequence in sequences:
                print(f">{sequence_id}_{counter}\n{sequence}")
                counter += 1
