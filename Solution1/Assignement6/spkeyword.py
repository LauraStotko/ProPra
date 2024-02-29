#!/usr/bin/python3

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="List entries from Swissprot file based on given keywords.")
    parser.add_argument("--keyword", nargs='+', help="List of keywords for filtering", required=True)
    # 'nargs': + since we accept one or more values
    parser.add_argument("--swissprot", type=argparse.FileType('r'), help="Swissprot file", required=True)
    return parser.parse_args()


def parse_entry_keywords(line):
    list_of_entries_keys = []
    line = line.strip('KW   ')
    line = line.replace('.', ';')

    for single_keyword in line.split(';'):
        if len(single_keyword) != 0:
            if single_keyword[0].isspace():
                single_keyword = single_keyword[1:]
            list_of_entries_keys.append(single_keyword)

    return list_of_entries_keys


def parse_entry_ac(line):
    ac_list = []
    line = line.strip('AC   ')

    for ac_number in line.split(';'):
        if len(ac_number) != 0:
            ac_number = ac_number.strip()
            ac_list.append(ac_number)
    return ac_list


def print_ac_list(list_of_all_acs):
    for ac_nr in list_of_all_acs:
        print(ac_nr)


def main():
    args = parse_arguments()

    # Get keywords & save as set to remove duplicates
    keywords = set(args.keyword)

    # List of all AC numbers
    all_ac_numbers = []

    list_of_entry_keywords = []
    list_of_entry_ac = []
    found_matching_keywords = False

    # Get each entry from the Swissprot file
    # Each entry is seperated by '//'
    for line in args.swissprot.read().splitlines():

        if line.startswith('KW'):
            list_of_entry_keywords.extend(parse_entry_keywords(line))

        if line.startswith('AC'):
            list_of_entry_ac.extend(parse_entry_ac(line))

        if line.startswith('//'):

            for current_keyword in list_of_entry_keywords:

                for input_keyword in keywords:
                    if current_keyword == input_keyword:
                        found_matching_keywords = True

            if found_matching_keywords:
                all_ac_numbers.extend(list_of_entry_ac)

            list_of_entry_keywords = []
            list_of_entry_ac = []
            found_matching_keywords = False

    for current_keyword in list_of_entry_keywords:

        for input_keyword in keywords:
            if current_keyword == input_keyword:
                found_matching_keywords = True

    if found_matching_keywords:
        all_ac_numbers.extend(list_of_entry_ac)

    cleaned_ac_numbers = list(set(all_ac_numbers))
    cleaned_ac_numbers.sort()

    for ac_nr in cleaned_ac_numbers:
        print(ac_nr)


if __name__ == "__main__":
    main()
