#!/usr/bin/python3
import argparse
import urllib.request

def acsearch(number):
    # link with the corresponding AC number
    url = f"https://rest.uniprot.org/uniprotkb/{number}.fasta"
    # try and except, in case the ac number is not valid
    try:
        fasta = urllib.request.urlopen(url)
        # 200 is the code for valid website
        if fasta.getcode() == 200:
            # open fasta file and decodes the content as UTF-8 encoded text
            return fasta.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print("Sorry, this SwissProt AC-number does not exist")
        return None

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Download the sequence to a SwissProt AC number and receive it in FASTA format")
    pars.add_argument("--ac", help="SwissProt AC-number")
    args = pars.parse_args()
    if args.ac:
        fasta = acsearch(args.ac)
        if fasta is not None:
            print(fasta.strip())
