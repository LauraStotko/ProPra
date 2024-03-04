#!/usr/bin/env python3

import argparse


def read_sam_file(sam_file): # SAM-Datei einlesen
    sequences = []
    for line in sam_file:  # Direktes Lesen aus dem übergebenen Dateistream
        if not line.startswith('@'):  # Ignore header lines.
            parts = line.strip().split('\t')
            if '*' == parts[2]:  # Filter sequences without valid alignment.
                sequences.append(parts)
    return sequences


def get_off_and_mismatches(sam_file):  # Filter sequences with mismatches in GG suffix.
    no_off_targets = []
    mismatch_sequences=[]
    for line in sam_file:
        if line.startswith('@'):  # Ignore header lines.
            continue
        parts = line.split('\t')
        if '*' == parts[2]:
            no_off_targets.append(parts)
        else:
            md_tag = get_md_tag(line)
            if md_tag and check_for_mismatch_in_md_tag(md_tag):
                mismatch_sequences.append(line.split("\t"))
    return no_off_targets,mismatch_sequences


def write_fasta(sequences, output_file):
    with open(output_file, 'w') as file:
        for seq in sequences:
            header = f">{seq[0]}"  # Extract header from SAM file.
            sequence = seq[9]  # Extract sequence from SAM file.
            file.write(f"{header}\n{sequence}\n")


def check_for_mismatch_in_md_tag(md_tag):
    # MD Tag Format: MD:Z:4C0A  -> 4C0A sind die Mismatches
    number = ""
    for char in md_tag[::-1]: # umdrehen der Liste und durchlaufen
        if not char.isdigit(): # führt zu einem Abbruch, wenn das Zeichen kein numerisches Zeichen ist
            break
        else:
            number = char + number
    return int(number) < 2

def get_md_tag(sam_line): # MD Tag aus SAM Zeile extrahieren
    for field in sam_line.split("\t"):
        if "MD" in field:
            return field


def main():
    parser = argparse.ArgumentParser(description="Filter SAM file and output FASTA file based on specific criteria.")
    parser.add_argument("--sam", type=argparse.FileType('r'), required=True, help="Input SAM file.")
    parser.add_argument("--no-off-targets", type=str, required=True,
                        help="Output FASTA file for sequences with valid alignments.")
    parser.add_argument("--with-mismatch", type=str, required=True,
                        help="Output FASTA file for sequences with mismatches in GG suffix.")
    args = parser.parse_args()

    sequences,mismatch_seqs= get_off_and_mismatches(args.sam)
    write_fasta(sequences, args.no_off_targets)  # Erste FASTA-Datei nach gültiger Ausrichtung
    write_fasta(mismatch_seqs, args.with_mismatch)  # Zweite FASTA-Datei nach Mismatch-Filterung


if __name__ == "__main__":
    main()
