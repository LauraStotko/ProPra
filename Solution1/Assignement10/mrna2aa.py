#!/usr/bin/python3
import argparse
import sys

def read_fasta(fasta_file):
    sequences = {}
    with open(fasta_file) as f:
        current_id = None
        current = ''
        for l in f:
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

def translate_codon(codon):
    codon_table = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    return codon_table.get(codon, 'X')


def translate_mrna(mrna_sequences):
    protein_sequences = []
    for sequence_id, sequence in mrna_sequences.items():
        if len(sequence) % 3 != 0:
            break  # Sequenzlänge ist nicht durch 3 teilbar

        protein_sequence = ''

        for i in range(0, len(sequence), 3):
            codon = sequence[i:i + 3]
            aa = translate_codon(codon)
            if aa == '*':
                break  # Stop-Codon
            elif aa == 'X':
                protein_sequence = None
                break
            else:
                protein_sequence += aa
        if protein_sequence is not None:
            protein_sequences[sequence_id] = protein_sequence

    return protein_sequences

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Translate mRNA to Proteins")
    pars.add_argument("--fasta", type=str,required=True)
    args = pars.parse_args()

    if args.fasta =='-':
        fasta_file = sys.stdin
        sequences = read_fasta(fasta_file)
    else:
        sequences = read_fasta(args.fasta)

    protein_sequences = translate_mrna(sequences)

    for sequence_id, protein_sequence in protein_sequences:
        print(f'>{sequence_id}')
        print(protein_sequence)

