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



if __name__ == '__main__':
    pars = argparse.ArgumentParser(description="Download the sequence to a SwissProt AC number and receive it in FASTA format")
    pars.add_argument("--id", help="PDB ID")
    pars.add_argument("--output", help="output type")
    args = pars.parse_args()

    pdb_content = download_pdb(args.id)


    #output auf konsole
    if args.output == '-':
        print(pdb_content.strip())
    else:                       #output als file
        path = f"{args.output}/{args.id}.pdb"
        with open(path, 'w') as f:
            f.write(pdb_content)
            f.close()




