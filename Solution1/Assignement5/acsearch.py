#!/usr/bin/python3
import argparse
import urllib.request

def acsearch(number):
    url = f"https://rest.uniprot.org/uniprotkb/{number}.fasta"
    try:
        fasta = urllib.request.urlopen(url)
        if fasta.getcode() == 200:
            return fasta.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print("Sorry, this SwissProt AC-number does not exist")
        return None

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Download the sequence to a SwissProt AC number and receive it in FASTA format")
    pars.add_argument("--ac", help="SwissProt AC-number")
    args = pars.parse_args()
    fasta = acsearch(args.ac)
    if fasta is not None:
        print(fasta.strip())
