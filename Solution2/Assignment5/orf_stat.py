#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plot
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


def filter_orfs(sequences, lower, upper):
    count = 0
    filtered_orfs = {}
    for sequence_id, sequence in sequences.items():
       number = len(sequence) // 3 - 1      # for the stop codon
       if lower <= number <= upper:
            filtered_orfs[sequence_id] = sequence
            count += 1

    return filtered_orfs

def plot_histogram(filtered_orfs, lower, upper, bins, path):
    length = []

    for sequence_id, sequence in filtered_orfs.items():
        length.append(len(sequence)//3)

    plot.hist(length, bins=bins, range=(lower,upper), color='blue')
    plot.xlabel('ORF Length')
    plot.ylabel('Count')
    plot.title('Histogram of ORF Lengths')
    plot.savefig(path)
    plot.show()
    return plot



if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="")
    pars.add_argument("--fasta", type=argparse.FileType('r'), required=True)    # orf file
    pars.add_argument("--histogram", help="path to output file", required=False)
    pars.add_argument("--lower", type=int, required=True)
    pars.add_argument("--upper", type=int, required=True)
    pars.add_argument("--bins", type=int, required=True)

    args = pars.parse_args()

    sequences = read_fasta(args.fasta)
    filtered_orfs = filter_orfs(sequences, args.lower, args.upper)
    count = len(filtered_orfs)


    if args.histogram:
        path = f"{args.histogram}/output.png"
        plot_histogram(filtered_orfs, args.lower, args.upper, args.bins, path)
        print(count)
    else:
        print(count)