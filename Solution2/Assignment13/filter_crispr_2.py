#!/usr/bin/env python3

import argparse
import sys

def read_sam_file(sam_file):
    sequences = []
    for line in sam_file: # Direktes Lesen aus dem übergebenen Dateistream
        if not line.startswith('@'): # Ignore header lines.
            parts = line.strip().split('\t')
            if '*' not in parts[5]: # Filter sequences without valid alignment.
                sequences.append(parts)
    return sequences

def filter_sequences_with_mismatches(sequences): # Filter sequences with mismatches in GG suffix.
    filtered_seqs = []
    for seq in sequences:
        tags = {tag.split(':')[0]: tag.split(':')[-1] for tag in seq[11:]} # Extract tags from SAM file.
        if 'NM' in tags and int(tags['NM']) <= 3 and seq[9].endswith('GG'): # Filter sequences with mismatches in GG suffix.
            filtered_seqs.append(seq)
    return filtered_seqs

def write_fasta(sequences, output_file):
    with open(output_file, 'w') as file:
        for seq in sequences:
            header = f">{seq[0]}" # Extract header from SAM file.
            sequence = seq[9] # Extract sequence from SAM file.
            file.write(f"{header}\n{sequence}\n")

def main():
    parser = argparse.ArgumentParser(description="Filter SAM file and output FASTA file based on specific criteria.")
    parser.add_argument("--sam", type=argparse.FileType('r'), required=True, help="Input SAM file.")
    parser.add_argument("--no-off-targets", type=str, required=True, help="Output FASTA file for sequences with valid alignments.")
    parser.add_argument("--with-mismatch", type=str, required=True, help="Output FASTA file for sequences with mismatches in GG suffix.")
    args = parser.parse_args()

    sequences = read_sam_file(args.sam)
    write_fasta(sequences, args.no_off_targets) # Erste FASTA-Datei nach gültiger Ausrichtung

    mismatch_seqs = filter_sequences_with_mismatches(sequences)
    write_fasta(mismatch_seqs, args.with_mismatch) # Zweite FASTA-Datei nach Mismatch-Filterung

if __name__ == "__main__":
    main()
