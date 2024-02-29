#!/usr/bin/python3

import argparse
import re



def parse_arguments():
    parser = argparse.ArgumentParser(description="Find the PROSITE pattern in FASTA sequences.")
    parser.add_argument("--fasta", type=argparse.FileType("r"), help="Input FASTA file or '-' for stdin", required=True)
    parser.add_argument("--pattern", type=str, help="PROSITE pattern to search for", required=True)
    return parser.parse_args()


def prosite_to_regex(prosite_pattern):
    regex_pattern = prosite_pattern
    regex_pattern = regex_pattern.replace('-', '')  # Separation between different elements
    regex_pattern = regex_pattern.replace(' - ', '')
    regex_pattern = regex_pattern.replace('x', '.')  # Any character except newline
    regex_pattern = regex_pattern.replace('{', '[^')  # [^abc] ->	not a, b, or c
    regex_pattern = regex_pattern.replace('}', ']')
    regex_pattern = regex_pattern.replace('(', '{')  # a{5}	exactly five
    regex_pattern = regex_pattern.replace(')', '}')
    regex_pattern = regex_pattern.replace('<', '^')  # ^abc$	start / end of the string
    regex_pattern = regex_pattern.replace('>', '$')

    regex_pattern = regex_pattern.replace('?', '.')
    regex_pattern = regex_pattern.replace('*', '.*?')  # '.*?' matches any number of any character, even zero (non-greedy -> shortest possible match)
    return regex_pattern



def parse_fasta(fasta_file):
    key = ''
    sequence = ''
    dict_sequences = {}

    for line in fasta_file:

        if line.startswith('>'):
            if key not in dict_sequences:
                if key != "":
                    dict_sequences[key] = sequence

                sequence = ''
                key = line.strip('\n')
                key = key.strip('>')
                key = key.strip('\t')

        else:
            sequence += line.strip()

    dict_sequences[key] = sequence
    #print(f'Key: {key}  Sequence: {sequence}')

    # print(key)

    return dict_sequences


def find_prosite_patterns(dict_sequences, pattern):
    regex_pattern = re.compile(pattern)

    # print(f'Pattern: {regex_pattern.pattern}')

    matches = []

    for key, value in dict_sequences.items():

        # Go through sequence

        for i in range(len(value)):
            for j in range(i, len(value) + 1):

                match = regex_pattern.fullmatch(value[i:j])

                if match:
                    matches.append({'key': key.strip(), 'start': i, 'sequence': match.group()})


    return matches


def main():
    args = parse_arguments()

    # print(f'FASTA File: {args.fasta.name}')

    prosite_pattern = args.pattern
    # print(f'Pattern: {prosite_pattern}')

    pattern = prosite_to_regex(prosite_pattern)
    # print(f'Pattern as RegEx: {regex_pattern}')


    dict_sequences = parse_fasta(args.fasta)

    matches = find_prosite_patterns(dict_sequences, pattern)

    for match in matches:
        print(f'{match["key"]}\t{match["start"]}\t{match["sequence"]}')



if __name__ == "__main__":
    main()
