#!/usr/bin/env python3

import argparse
import sys 

def read_fasta(file_handle):
    sequences = {} # Initializes an empty dictionary to store the sequences
    current_seq = ''
    seq_id = ''
    for line in file_handle: # Iterates over each line in the file
        line = line.strip()
        if line.startswith('>'):
            if current_seq:
                sequences[seq_id] = current_seq
                current_seq = ''
            seq_id = line[1:]  # Removes the '>' character
        else:
            current_seq += line
    if current_seq:
        sequences[seq_id] = current_seq
    return sequences

def find_unique_sequences(sequences, ks, start_index=None):
    unique_counts = {}
    for k in ks: # Iterates over each value of k
        seen = {} # Initializes a dictionary to store the subsequences and the genes they are found in
        unique_in_gene = {} # Initializes a dictionary to store whether a sequence is unique in a gene
        for seq_id, seq in sequences.items():
            unique_in_gene[seq_id] = False # Initializes each gene as not having a unique sequence
            if start_index is not None and start_index + k <= len(seq):
                subseq = seq[start_index:start_index + k]
                if subseq not in seen:
                    seen[subseq] = {seq_id}
                else:
                    seen[subseq].add(seq_id)
            elif start_index is None:
                for i in range(len(seq) - k + 1):
                    subseq = seq[i:i + k]
                    if subseq in seen:
                        seen[subseq].add(seq_id)
                    else:
                        seen[subseq] = {seq_id}

        # Determine if a subsequence is unique in a gene
        for subseq, ids in seen.items():
            if len(ids) == 1:
                unique_in_gene[list(ids)[0]] = True

        # Count the genes with at least one unique sequence
        unique_counts[k] = sum(unique_in_gene.values())
    return unique_counts

def main():
    parser = argparse.ArgumentParser(description='Identifies unique base sequences in genes.')
    parser.add_argument('--fasta', type=argparse.FileType('r'), default=sys.stdin,
                        help='Path to FASTA file or "-" for StdIn')
    parser.add_argument('--k', nargs='+', type=int, help='Values of k', required=True)
    parser.add_argument('--start', type=int, default=None, help='Start index for searching unique sequences')
    args = parser.parse_args()

    sequences = read_fasta(args.fasta) # Reads the FASTA file
    unique_counts = find_unique_sequences(sequences, args.k, args.start)

    # Print results
    for k, count in sorted(unique_counts.items()):
        print(f"{k}\t{count}")

if __name__ == '__main__':
    main()
