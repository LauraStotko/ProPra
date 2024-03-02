#!/usr/bin/env python

import argparse
import re


def read_sam_file(sam_file):
    # Liest eine SAM-Datei und extrahiert Sequenzen mit gültigem Alignment.
    """
    Argumente:
        sam_file (str): Pfad zur SAM-Datei.

    Rückgabe:
        sequences (list): Liste von Tupeln, jedes Tupel enthält die Read-ID und die Sequenz.
    """
    sequences = []  # Initialisiere die Liste für die gesammelten Sequenzen.
    with open(sam_file, 'r') as file:
        for line in file:
            if not line.startswith('@'):  # Ignoriere Header-Zeilen.
                parts = line.split('\t')  # Teile die Zeile in ihre Komponenten.
                cigar_string = parts[5]  # Die CIGAR-Zeichenkette befindet sich in der 6. Spalte.
                if '*' not in cigar_string:  # Filtere Sequenzen ohne gültiges Alignment aus.
                    sequences.append((parts[0], parts[9]))  # Füge die Read-ID und die Sequenz zur Liste hinzu.
    return sequences

def find_crispr_sequences(sequences, crispr_regex=r"(?=(.{20}[ACGT]GG))"):
    crispr_matches = {}
    for seq_id, seq in sequences:
        matches = list(re.finditer(crispr_regex, seq))
        if matches:
            crispr_matches[seq_id] = [(m.start(1), m.group(1)) for m in matches]
    return crispr_matches

def write_fasta(crispr_matches, no_off_targets_filename):
    with open(no_off_targets_filename, 'w') as no_off_file:
        for seq_id, matches in crispr_matches.items():
            for position, match in matches:
                no_off_file.write(f">{seq_id}:{position}\n{match}\n")

def main():
    parser = argparse.ArgumentParser(description='Filter CRISPR alignments and extract sequences into FASTA format.')
    parser.add_argument('--input-sam', type=str, required=True, help='Input SAM file path.')
    parser.add_argument('--output-no-off-targets', type=str, required=True, help='Output FASTA file path for sequences without off-targets.')
    parser.add_argument('--output-with-mismatch', type=str, required=True, help='Output FASTA file path for sequences with mismatches in the GG-suffix.')

    args = parser.parse_args()

    sequences = read_sam_file(args.input_sam)
    crispr_matches = find_crispr_sequences(sequences)
    write_fasta(crispr_matches, args.output_no_off_targets)

if __name__ == "__main__":
    main()



