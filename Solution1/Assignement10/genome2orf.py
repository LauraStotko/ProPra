#!/usr/bin/python3
import argparse

def read_fasta(fasta_file):
    sequences = {}

    current_id = None
    current = ''
    # go trough every line of the file and save the sequence_id with the corresponding sequence in a dictionary
    for l in fasta_file:
        #returns the same string without spaces
        l = l.strip()
        # first line of new sequence, contains the sequence_id
        if l.startswith('>'):
            if current_id:
                sequences[current_id] = current
                current=''
            #save new id
            current_id = l.strip()[1:]
        else:
            # add line of sequence to the current sequence
            current += l
    if current_id:
        sequences[current_id] = current
    return sequences

def get_features(features_table):
    features_cds = {}

    # save only the line in feature_table that contain CDS and do not start with hashtag
    for l in features_table:
        # head line
        if l.startswith('#'):
            continue
        columns = l.strip().split('\t')
        if not columns[0] == 'CDS':
            continue
        # save columns from feature table that are important for next step
        locus_tag = columns[16]
        start = int(columns[7])
        end = int(columns[8])
        strand = columns[9]
        sequence_id = columns[6]
        if sequence_id not in features_cds:
            features_cds[sequence_id]=[]
        features_cds[sequence_id].append((locus_tag, start, end, strand))

    return features_cds

def genome2orf(genome_file, feature_file):
    # receive content of files as dictionaries
    sequences = read_fasta(genome_file)
    features_cds = get_features(feature_file)
    orf_sequences = {}

    # receive orfs for every sequence_id in the features_cds
    for sequence_id, features in features_cds.items():
        key = None
        for seq in sequences.keys():
            if sequence_id in seq:
                key = seq
        if key:
            seq = sequences.get(key)
            for feature in features:
                locus_tag, start, end, strand = feature
                if strand == '-':
                    # negative strand
                   current = reverse_complement(seq[start-1:end])
                    # flip the string zo receive the reverse complement
                   current = current[::-1]
                else:
                   current = seq[start-1:end]
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
    return result_sequence

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Extracting ORFs from a genome sequence")
    pars.add_argument("--organism", type= argparse.FileType('r'), required=True)
    pars.add_argument("--features", type= argparse.FileType('r'), required=True)
    args = pars.parse_args()

    orf_sequences = genome2orf(args.organism, args.features)

    for locus_tag, sequence in orf_sequences.items():
        print(f'>{locus_tag}')
        print(sequence)