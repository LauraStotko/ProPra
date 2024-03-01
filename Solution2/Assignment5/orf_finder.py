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

def find_orfs(sequences):
    orf_sequences = {}
    stop_codons = ["TAA", "TAG", "TGA"]
    start_codon="ATG"

    for sequence_id, sequence in sequences.items():
        orf_sequence = ''
        # zählt die wievielte orf sequence es bereits ist für den Namen
        counter=0
        i = 0
        # einser schritte, um überlappende zu finden, erst in dreier schritten, wenn ATG gefunden
        while i in range(len(sequence)):
            if sequence[i:i+3] != start_codon:
                i += 1
                continue
            #i+3 ist Start Codon
            orf_sequence += sequence[i:i+3]
            for j in range(i+3,len(sequence),3):
                # um i danach zu aktualisieren
                if sequence[j:j+3] in stop_codons:
                    orf_sequence += sequence[j:j+3]
                    i = j+3
                    break
                orf_sequence += sequence[j:j+3]
            # ich lande immer nur hier, wenn ich ein Start Codon gefunden habe
            orf_sequences[f"{sequence_id}_{counter}"] = orf_sequence
            counter += 1
            orf_sequence = ''
    return orf_sequences


if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Find ORFs")
    pars.add_argument("--fasta", type=argparse.FileType('r'), required=True)
    pars.add_argument("--output", help= "path to output file", required=False)
    # add other arguments
    args = pars.parse_args()

    sequences = read_fasta(args.fasta)
    orf_sequences = find_orfs(sequences)

    # ATG ist Start Codon, TAA/ ist Stop Codon
    # Also ich muss die sequenz in einsere Schritten durchlaufen bis ATG gefunden dann in dreier Schritten bis Stopp Codon, damit auch überlappende entdeckt werden
    if args.output:
        path = f"{args.output}/{args.fasta.name}"
        with open(path, 'w') as f:
            for sequence_id, sequence in orf_sequences.items():
                f.write(f">{sequence_id}\n{sequence}")
            f.close()
    else:
        # print sequences on commmand line
        for sequence_id, sequence in orf_sequences.items():
            print(f">{sequence_id}\n{sequence}")
