#!/usr/bin/env python3

from argparse import ArgumentParser

def parse_arguments():
    # Parse command line arguments.
    parser = ArgumentParser(description="Filter SAM file and output FASTA file.")
    parser.add_argument("--sam", type=str, required=True, help="Input SAM file.")
    parser.add_argument("--no-off-targets", type=str, help="Output FASTA file for sequences without off-targets.")
    parser.add_argument("--with-mismatch", type=str, help="Output FASTA file for sequences with mismatches.")
    return parser.parse_args()


def read_sam_file(sam_file):
    # Liest eine SAM-Datei und extrahiert Sequenzen mit gültigem Alignment.
    sequences = []  # Initialisiere die Liste für die gesammelten Sequenzen.
    with open(sam_file, 'r') as file:
        for line in file:
            if not line.startswith('@'):  # Ignoriere Header-Zeilen.
                parts = line.split('\t')  # Teile die Zeile in ihre Komponenten.
                cigar_string = parts[5]  # Die CIGAR-Zeichenkette befindet sich in der 6. Spalte.
                if '*' not in cigar_string:  # Filtere Sequenzen ohne gültiges Alignment aus.
                    sequences.append((parts[0], parts[9]))  # Füge die Read-ID und die Sequenz zur Liste hinzu.
    return sequences


def filter_sequences(sequences, with_mismatch=False):
    # Filter sequences based on presence of mismatches.
    filtered_seqs = []
    for seq in sequences:
        # Assuming the optional fields start from index 11
        tags = {tag.split(':')[0]: tag.split(':')[-1] for tag in seq[11:]}
        if with_mismatch:
            # Include sequence if NM (edit distance) tag is present and greater than 0
            if 'NM' in tags and int(tags['NM']) > 0:
                filtered_seqs.append(seq)
        else:
            # Include sequence if NM tag is not present or 0
            if 'NM' not in tags or int(tags['NM']) == 0:
                filtered_seqs.append(seq)
    return filtered_seqs


def write_fasta(sequences, output_file):
    with open(output_file, 'w') as file:
        for seq in sequences:
            header = f">{seq[0]}"  # Use QNAME as header
            sequence = seq[9]  # SEQ field
            file.write(f"{header}\n{sequence}\n")


def main():
    args = parse_arguments()

    # Read and filter sequences
    sequences = list(read_sam_file(args.sam))
    if args.no_off_targets:
        filtered_seqs = filter_sequences(sequences, with_mismatch=False)
        write_fasta(filtered_seqs, args.no_off_targets)
    if args.with_mismatch:
        filtered_seqs = filter_sequences(sequences, with_mismatch=True)
        write_fasta(filtered_seqs, args.with_mismatch)

if __name__ == "__main__":
    main()
