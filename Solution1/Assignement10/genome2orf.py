#!/usr/bin/python3
import argparse

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

def get_features(features_table):
    features_cds = {}

    with open(features_table, 'r') as features:
        for l in features:
            if l.startswith('#'):
                continue
            columns = l.strip().split('\t')
            if not columns[0] == 'CDS':
                continue
            locus_tag = columns[16]
            start = int(columns[7])-1
            end = int(columns[8])
            strand = columns[9]
            sequence_id = columns[6]
            if sequence_id not in features_cds:
                features_cds[sequence_id]=[]
            features_cds[sequence_id].append((locus_tag, start, end, strand))

    return features_cds

def genome2orf(genome_file, feature_file):
    sequences = read_fasta(genome_file)
    features_cds = get_features(feature_file)
    orf_sequences = {}

    for sequence_id, features in features_cds.items():
        current = ''
        seq = sequences.get(sequence_id)
        if seq:
            for feature in features:
                locus_tag, start, end, strand = feature
                if strand == '-':
                   current = reverse_complement(seq[end:start])
                else:
                   current = seq[start:end]
                orf_sequences[locus_tag] = current
    return orf_sequences

def reverse_complement(sequence):
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
    pars = argparse.ArgumentParser(description="Extracting ORFs from a genome sequence")
    pars.add_argument("--organism", type=str, required=True)
    pars.add_argument("--features", type=str, required=True)
    args = pars.parse_args()

    orf_sequences = genome2orf(args.organism, args.features)

    for locus_tag, sequence in orf_sequences.items():
        print(f'>{locus_tag}')
        print(sequence)