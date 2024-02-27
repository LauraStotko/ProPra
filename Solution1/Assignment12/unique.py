#!/usr/bin/env python3

import argparse
import sys


def read_fasta(file_handle):
    """Liest FASTA-Datei von einem Dateihandle und gibt Sequenzen zurück."""
    sequences = {}
    current_seq = ''
    seq_id = ''
    for line in file_handle:
        line = line.strip()
        if line.startswith('>'):
            if current_seq:
                sequences[seq_id] = current_seq
                current_seq = ''
            seq_id = line[1:]  # Entfernt das '>' Zeichen
        else:
            current_seq += line
    if current_seq:
        sequences[seq_id] = current_seq
    return sequences


def find_unique_sequences(sequences, ks):
    """Findet einzigartige Sequenzen für verschiedene k und zählt eindeutige Gene."""
    unique_counts = {}
    for k in ks:
        seen = {}
        unique_in_gene = {}
        for seq_id, seq in sequences.items():
            unique_in_gene[seq_id] = False
            for i in range(len(seq) - k + 1):
                subseq = seq[i:i + k]
                if subseq in seen:
                    seen[subseq].add(seq_id)
                else:
                    seen[subseq] = {seq_id}

        # Bestimme, ob eine Subsequenz einzigartig in einem Gen ist
        for subseq, ids in seen.items():
            if len(ids) == 1:
                unique_in_gene[list(ids)[0]] = True

        # Zähle die Gene mit mindestens einer einzigartigen Sequenz
        unique_counts[k] = sum(unique_in_gene.values())
    return unique_counts


def main():
    parser = argparse.ArgumentParser(description='Identifiziert einzigartige Basenfolgen in Genen.')
    parser.add_argument('--fasta', type=argparse.FileType('r'), default=sys.stdin,
                        help='Pfad zur FASTA-Datei oder "-" für StdIn')
    parser.add_argument('--k', nargs='+', type=int, help='Werte von k', required=True)
    args = parser.parse_args()

    sequences = read_fasta(args.fasta)
    unique_counts = find_unique_sequences(sequences, args.k)

    # Ergebnisse ausgeben
    for k, count in sorted(unique_counts.items()):
        print(f"{k}\t{count}")


if __name__ == '__main__':
    main()
