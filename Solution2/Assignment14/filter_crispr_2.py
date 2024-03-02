#!/usr/bin/env python3

from argparse import ArgumentParser

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
    filtered_seqs = []
    for seq in sequences: # Iteriere über alle Sequenzen
        tags = {tag.split(':')[0]: tag.split(':')[-1] for tag in seq[11:]} # Extrahiere die Tags und speichere sie in einem Dictionary
        if with_mismatch:
            if 'NM' in tags and int(tags['NM']) > 0: # Überprüfe, ob die Sequenz Mismatches enthält
                filtered_seqs.append(seq)
        else:
            if 'NM' not in tags or int(tags['NM']) == 0: # Überprüfe, ob die Sequenz keine Mismatches enthält
                filtered_seqs.append(seq)
    return filtered_seqs


def write_fasta(sequences, output_file):
    with open(output_file, 'w') as file:
        for seq in sequences:
            header = f">{seq[0]}"  # Use QNAME as header
            sequence = seq[9]  # SEQ field
            file.write(f"{header}\n{sequence}\n")


def main():
    parser = ArgumentParser(description="Filter SAM file and output FASTA file.")
    parser.add_argument("--sam", type=str, required=True, help="Input SAM file.")
    parser.add_argument("--no-off-targets", type=str, help="Output FASTA file for sequences without off-targets.")
    parser.add_argument("--with-mismatch", type=str, help="Output FASTA file for sequences with mismatches.")
    return parser.parse_args()

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
