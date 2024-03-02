#!/usr/bin/env python3

import argparse
import re


def read_fasta(file):
    sequences = {}
    current_seq_name = None
    for line in file:
        line = line.strip()
        if not line:  # Ignoriere leere Zeilen
            continue
        if line.startswith(">"): # überprüft, ob eine Zeile mit dem Zeichen > beginnt
            current_seq_name = line[1:] # entfernt das > Zeichen am Anfang der Zeile und speichert den Rest der Zeile als current_seq_name
            sequences[current_seq_name] = "" # initialisiert ein neues Element im sequences Dictionary mit dem Schlüssel current_seq_name
        elif current_seq_name:
            sequences[current_seq_name] += line # leerer String wird mit Sequenzdaten gefüllt
    return sequences

"""
def find_crispr_sequences(sequences):
    crispr_regex = r"(.{20}[ACGT]GG)" # definiert eine CRISPR/Cas-Erkennungssequenz als regulären Ausdruck
    crispr_matches = {} # initialisiert ein leeres Dictionary, um die Übereinstimmungen zu speichern
    for seq_name, seq in sequences.items(): # iteriert über alle Sequenzen, seq_name ist der Name der Sequenz und seq ist die Sequenz selbst
        matches = list(re.finditer(crispr_regex, seq)) # sucht nach allen Übereinstimmungen des regulären Ausdrucks in der Sequenz
        if matches:
            crispr_matches[seq_name] = [(match.start() + 1, match.group(1)) for match in matches]
    return crispr_matches
"""

def find_crispr_sequences(sequences):
    crispr_regex = r"(?=(.{20}[ACGT]GG))" # Aktualisierter regulärer Ausdruck für Überlappungen
    crispr_matches = {}
    for seq_name, seq in sequences.items():
        matches = list(re.finditer(crispr_regex, seq))
        if matches:
            crispr_matches[seq_name] = [(match.start() + 1, match.group(1)) for match in matches]
    return crispr_matches



def format_sequences_in_fasta(crispr_matches):
    fasta_formatted_str = ""  # initialisiert einen leeren String, um die formatierten Sequenzen zu speichern
    for seq_name, matches in crispr_matches.items():  # iteriert über alle gefundenen Übereinstimmungen
        for start_position, matched_seq in matches:  # iteriert über jede Übereinstimmung
            # Formatierung gemäß der neuen Spezifikation
            fasta_formatted_str += f">{seq_name}\t{start_position}\n{matched_seq}\n"
    return fasta_formatted_str


def main():
    parser = argparse.ArgumentParser(description="Findet CRISPR/Cas-Erkennungssequenzen in FASTA-Dateien.")
    parser.add_argument('--fasta', type=argparse.FileType('r'), required=True, help="Pfad zur FASTA-Datei")
    parser.add_argument('--output', type=str, required=True, help="Pfad zur Ausgabedatei")
    args = parser.parse_args()

    sequences = read_fasta(args.fasta)
    crispr_matches = find_crispr_sequences(sequences)
    fasta_formatted_str = format_sequences_in_fasta(crispr_matches)

    # Schreiben der formatierten Sequenzen in eine Datei
    with open(args.output, 'w') as output_file:
        output_file.write(fasta_formatted_str)


if __name__ == "__main__":
    main()