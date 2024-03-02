#!/usr/bin/python3
import argparse
import urllib.request

def download_pdb(id):
    url = f"https://files.rcsb.org/view/{id}.pdb"
    try:
        pdb = urllib.request.urlopen(url)
        # 200 is the code for valid website
        if pdb.getcode() == 200:
            # open fasta file and decodes the content as UTF-8 encoded text
            return pdb.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print("Sorry, this PDB ID does not exist")
        return None

def download_as_fasta(id):
    url = f"https://www.rcsb.org/fasta/entry/{id}/display"
    try:
        fasta = urllib.request.urlopen(url)
        if fasta.getcode()==200:
            return fasta.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print("Sorry, this PDB ID does not exist")
        return None

if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Download the PDB file to a PDB id")
    pars.add_argument("--id", help="PDB ID", required=True)
    pars.add_argument("--output", help="output type", required = True)
    pars.add_argument("--fasta", help = "Output as fasta", required=False)
    args = pars.parse_args()

    if args.fasta:
        content = download_as_fasta(args.id)
    else:
        content = download_pdb(args.id)

    if content is not None:
        #output auf konsole
        if args.output == '-':
            print(content.strip())
        else:                       #output als file
            path = f"{args.output}/{args.id}.pdb"
            with open(path, 'w') as f:
                f.write(content)
                f.close()


