#!/usr/bin/python3

import argparse
import re

import requests


def parse_arguments():
    parser = argparse.ArgumentParser(description="Find the PROSITE pattern in FASTA sequences.")
    parser.add_argument("--fasta", type=argparse.FileType("r"), help="Input FASTA file or '-' for stdin", required=True)
    parser.add_argument("--pattern", type=str, help="PROSITE pattern to search for")
    parser.add_argument("--web", type=str, help="PROSITE ID to load pattern from web")
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
    dict_sequences = {}     # Store the parsed sequences as:    Key: sequence ID    Value: cleaned sequence

    for line in fasta_file:
        if line.startswith('>'):
            # If the line starts with '>' -> sequence ID
            if key not in dict_sequences:
                # Check if sequence ID is not already in the dictionary
                if key != "":
                    # If it's not the first sequence, add the previous sequence to the dictionary
                    dict_sequences[key] = sequence

                sequence = ''   # Reset the sequence variable for the new sequence
                key = line.strip('\n')
                key = key.strip('>')
                key = key.strip('\t')

        else:
            sequence += line.strip()

    dict_sequences[key] = sequence  # Add the last sequence to the dictionary

    return dict_sequences


def find_prosite_patterns(dict_sequences, pattern):
    regex_pattern = re.compile(pattern)

    # print(f'Pattern: {regex_pattern.pattern}')

    matches = []

    # Iterate through each sequence in the input dictionary
    for key, value in dict_sequences.items():

        # Iterate through all possible substrings in the sequence
        for i in range(len(value)):
            for j in range(i, len(value) + 1):

                # Attempt to match the current substring to the Prosite pattern
                match = regex_pattern.fullmatch(value[i:j])

                if match:
                    matches.append({'key': key.strip(), 'start': i, 'sequence': match.group()})

    return matches


def get_prosite_pattern(pattern, prosit_id):
    if pattern:
        return pattern
    elif prosit_id:
        return get_prosite_pattern_from_web(prosit_id)


def get_prosite_pattern_from_web(prosit_id):
    prosite_dat = download_prosite_dat()
    # Search for the Prosite ID (AC) in the downloaded prosite.dat
    ac_match = re.search(r"AC   " + prosit_id + r";", prosite_dat)

    if ac_match:
        return extract_pattern_from_prosite_dat(prosite_dat, prosit_id)


def download_prosite_dat():
    url = "https://ftp.expasy.org/databases/prosite/prosite.dat"
    prosite_dat = requests.get(url)

    # Check if the HTTP request was successful (status code 200)
    if prosite_dat.status_code == 200:
        return prosite_dat.text


def extract_pattern_from_prosite_dat(prosite_dat, prosit_id):
    entry_start = prosite_dat.find(f"AC   {prosit_id}")
    if entry_start != -1:
        # Find the end position of the AC entry (denoted by '//')
        entry_end = prosite_dat.find("//", entry_start)
        # Extract the text corresponding to the AC entry
        entry_text = prosite_dat[entry_start:entry_end].strip()
        '''
          r"PA   (.+?)\n": Matches lines starting with 'PA' and captures the content inside parentheses,
                           which represents the Prosite pattern. The non-greedy qualifier '?'
                           ensures that the match is as short as possible.
        '''
        pattern_match = re.search(r"PA   (.+?)\n", entry_text)
        if pattern_match:
            # Extract first capturing group of the matched Prosite pattern
            pattern = pattern_match.group(1).strip()
            # Remove '.' -> end of pattern
            return pattern[:-1]


def main():
    args = parse_arguments()

    prosite_pattern = get_prosite_pattern(args.pattern, args.web)

    #print(f'Prosite Pattern: {prosite_pattern}')

    pattern = prosite_to_regex(prosite_pattern)
    # print(f'Pattern as RegEx: {regex_pattern}')

    dict_sequences = parse_fasta(args.fasta)

    matches = find_prosite_patterns(dict_sequences, pattern)

    for match in matches:
        print(f'{match["key"]}\t{match["start"]}\t{match["sequence"]}')


if __name__ == "__main__":
    main()
