#!/usr/bin/python3

import argparse
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description="Find the PROSITE pattern in FASTA sequences.")
    parser.add_argument("--fasta", type=argparse.FileType("r"), help="Input FASTA file or '-' for stdin", required=True)
    parser.add_argument("--pattern", type=str, help="PROSITE pattern to search for", required=True)
    return parser.parse_args()


def prosite_to_regex(prosite_Pattern):
    regex_pattern = prosite_Pattern
    regex_pattern = regex_pattern.replace('-', '')      # Separation between different elements
    regex_pattern = regex_pattern.replace(' - ', '')
    regex_pattern = regex_pattern.replace('x', '.')     # Any character except newline
    regex_pattern = regex_pattern.replace('{', '[^')    # [^abc] ->	not a, b, or c
    regex_pattern = regex_pattern.replace('}', ']')
    regex_pattern = regex_pattern.replace('(', '{')     # a{5}	exactly five
    regex_pattern = regex_pattern.replace(')', '}')
    regex_pattern = regex_pattern.replace('<', '}')     # ^abc$	start / end of the string
    regex_pattern = regex_pattern.replace('>', '}')

    regex_pattern = regex_pattern.replace('?', '.')
    regex_pattern = regex_pattern.replace('*', '.*?')   # '.*?' matches any number of any character, even zero (non-greedy -> shortest possible match)

    return regex_pattern


def main():
    args = parse_arguments()

    # Test PROSITE pattern converted to regular expression
    print(prosite_to_regex('C-x(2,4)-C-x(3)-[LIVMFYWC]-x(8)-H-x(3,5)-H'))


if __name__ == "__main__":
    main()
