import argparse
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description="List entries from Swissprot file based on given keywords.")
    parser.add_argument("--keyword", nargs='+', help="List of keywords for filtering", required=True)
    # 'nargs': + since we accept one or more values
    parser.add_argument("--swissprot", type=argparse.FileType('r'), help="Swissprot file", required=True)
    return parser.parse_args()


def parse_swissprot_accession_number(ac_nr):
    """
    Parses a Swissprot entry to extract AC (Accession) numbers.

    Parameters:
    - ac_nr (str): The portion of the Swissprot entry containing the AC numbers.

    Returns:
    - list: A list of AC numbers extracted from the provided string.

    The function uses a regular expression to search for AC numbers in the provided string.
    Looks for the following pattern:
    - `AC   `: Matches the literal string "AC   ".
    - `(\w+)`: Captures group for multiple word characters -> represents AC number.
    - `;`: Matches semicolon at the end of each AC number.
    """
    ac_numbers = re.findall(r'AC   (\w+);', ac_nr)
    return ac_numbers


def main():
    args = parse_arguments()

    # Test the argument parsing
    print(f'Keyword: {args.keyword}')
    print(f'Swissprot File: {args.swissprot.name}')

    # Test extraction of AC numbers
    entry = """
    AC   A12345;
    AC   C67890;
    """
    ac_numbers = parse_swissprot_accession_number(entry)
    print(ac_numbers)


if __name__ == "__main__":
    main()
