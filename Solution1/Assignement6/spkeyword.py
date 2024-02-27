import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="List entries from Swissprot file based on given keywords.")
    parser.add_argument("--keyword", nargs='+', help="List of keywords for filtering", required=True)
    # 'nargs': + since we accept one or more values
    parser.add_argument("--swissprot", type=argparse.FileType('r'), help="Swissprot file", required=True)
    return parser.parse_args()


# Test the argument parsing
args = parse_arguments()
print(f'Keyword: {args.keyword}')
print(f'Swissprot File: {args.swissprot.name}')
