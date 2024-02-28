#!/usr/bin/env python3

import argparse


def read_fasta_sequence(file_obj):
    """Liest eine FASTA-Datei aus einer Datei und gibt die Sequenz ohne Zeilenumbrüche zurück."""
    sequence = ''
    for line in file_obj:
        if not line.startswith('>'):
            sequence += line.strip()
    return sequence


def count_sequence_occurrences(genome, sequences):
    sequence_counts = {sequence: 0 for sequence in sequences}
    for sequence in sequences:
        # Endlosloops vermeiden
        if len(sequence) == 0:
            continue
        start = 0  # Anfangsindex für die Suche festlegen
        while start < len(genome):
            pos = genome.find(sequence, start)
            if pos != -1:
                sequence_counts[sequence] += 1
                start = pos + 1  # Suche vom Index direkt nach dem Anfang der gefundenen Sequenz fortsetzen
            else:
                break  # Keine weiteren Übereinstimmungen gefunden
    return sequence_counts

def main():
    parser = argparse.ArgumentParser(description='Count the occurrences of sequences in a given genome.')
    parser.add_argument('--sequence', nargs='+', required=True, help='Sequences to search for in the genome')
    parser.add_argument('--genome', type=argparse.FileType('r'), required=True, help='FASTA file containing the genome sequence')
    args = parser.parse_args()

    genome_sequence = read_fasta_sequence(args.genome)

    sequence_counts = count_sequence_occurrences(genome_sequence, args.sequence)
    for sequence, count in sequence_counts.items():
        print(f"{sequence}: {count}")


if __name__ == "__main__":
    main()
    