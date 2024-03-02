#!/usr/bin/python3
import random
import argparse

def generate_sequence(length, gc):
    sequence = ''
    count = float(gc) * int(length)
    random_positions = []

    i = 0
    while i < count:
        i += 1
        random_number = random.randint(0, length - 1)
        while random_number in random_positions:
            random_number = random.randint(0, length - 1)
        random_positions.append(random_number)

    for i in range(length):
        if i in random_positions:
            sequence += random.choice('GC')
        else:
            sequence += random.choice('TA')

    return sequence
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

def calculate_gc_content(sequence):
    #to claculate the yeast GC content
    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence)

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="")
    pars.add_argument("--length", type=int, required=True)
    pars.add_argument("--gc", help=float, required=True)
    pars.add_argument("--seqname", help="path to output file", required=False)
    pars.add_argument("--fasta", type=argparse.FileType('r'), required=False)

    args = pars.parse_args()

    if (args.fasta):
        sequences = read_fasta(args.fasta)
        for sequence_id, sequence in sequences.items():
            gc_content = calculate_gc_content(sequence)
            print(f">{sequence_id}\n{gc_content}")

    sequence = generate_sequence(args.length, args.gc)

    if args.seqname:
        print(f">{args.seqname}\n{sequence}")
    else:
        print(sequence)
