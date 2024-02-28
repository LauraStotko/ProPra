#!/usr/bin/python3
import argparse

def read_fasta(fasta_file):

    sequences = {}
    current_id = None
    current = ''
    # go trough every line of the file and save the sequence_id with the corresponding sequence in a dictionary
    for l in fasta_file:
        # returns the same string without spaces
        l = l.strip()
        # first line of new sequence, contains the sequence_id
        if l.startswith('>'):
            if current_id:
                sequences[current_id] = current
                current = ''
            #save new id
            current_id = l.strip()[1:]
        else:
            #add line of sequence to the current sequence
            current += l
    if current_id:
        sequences[current_id] = current
    return sequences

'''
Genome 2 ORF
'''
def get_features(features_table):
    features_cds = {}

    #save only the line in feature_table that contain CDS and do not start with hashtag
    for l in features_table:
        # head line
        if l.startswith('#'):
            continue
        columns = l.strip().split('\t')
        if not columns[0] == 'CDS':
            continue
        #save columns from feature table that are important for next step
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
                    current = complement(seq[start-1:end])
                    # flip the string zo receive the reverse complement
                    current = current[::-1]
                else:

                    current = seq[start-1:end]
                orf_sequences[locus_tag] = current
    return orf_sequences

def complement(sequence):
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

'''
DNA 2 MRNA
'''
def dna2mrna(orf_sequences):
    sequences = orf_sequences
    mrna_sequences = {}

    for sequence_id, sequence in sequences.items():
        mrna = replace(sequence)
        #save in new dictionary
        mrna_sequences[sequence_id] = mrna
    return mrna_sequences


def replace(dna_sequence):
    mrna_sequence = ""
    # replace T with U for mrna
    for base in dna_sequence:
        if base == 'T':
            mrna_sequence += 'U'
        else:
            mrna_sequence += base
    return mrna_sequence


'''
MRNA 2 AA
'''
def translate_codon(codon):
    # Codon table contains all 64 codons and their one letter code for the right amino acid
    codon_table = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    # X als default value, falls
    return codon_table.get(codon, 'X')

def translate_mrna(mrna_sequences):
    protein_sequences = {}

    for sequence_id, sequence in mrna_sequences.items():
        if len(sequence) % 3 != 0:
            break  # Sequenzlänge ist nicht durch 3 teilbar

        protein_sequence = ''

        for i in range(0, len(sequence), 3):
            codon = sequence[i:i + 3]
            aa = translate_codon(codon)
            if aa == '*':
                break  # Stop-Codon
            elif aa == 'X':
                protein_sequence = None
                break
            else:
                protein_sequence += aa
        if protein_sequence is not None:
            protein_sequences[sequence_id] = protein_sequence

    return protein_sequences

if __name__ == '__main__':
    # Starte den workflow mit dem Einlesen der Genome Datei und der Features Tabelle
    pars = argparse.ArgumentParser(description="Extracting ORFs from a genome sequence")
    pars.add_argument("--organism", type=argparse.FileType('r'), required=True)
    pars.add_argument("--features", type=argparse.FileType('r'), required=True)
    args = pars.parse_args()

    name = args.organism.name

    #Erhalte die orf-Sequenzen, output ist ein dictionary mit den sequenc_ids und der entsprechenden ORF Sequenz
    orf_sequences = genome2orf(args.organism, args.features)

    #dna to mRNA, input are the orf_sequenes and output is a dictionary containing sequence_id and the mrna
    mrna_sequences = dna2mrna(orf_sequences)

    #translate the mrna_sequences to protein sequences, output is a dictionary containing sequence_id and the protein sequences
    protein_sequences = translate_mrna(mrna_sequences)

    filename = f'output_{name}'

    with open(filename, 'w') as f:
        for sequence_id, protein_sequence in protein_sequences.items():
            f.write(f'>{sequence_id}\n{protein_sequence}\n')
        f.close()



