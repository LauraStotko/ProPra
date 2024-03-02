#!/usr/env/bin python

import argparse
import requests

def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download PDB file for ID {pdb_id}")

# Dictionary für Aminosäure-Abkürzungen
aa_dict = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLU": "E",
    "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
    "TYR": "Y", "VAL": "V"
}

def parse_secondary_structure(pdb_data):
    ss_info = {}
    for line in pdb_data.splitlines():
        if line.startswith('HELIX'):
            chain = line[19]  # Extrahiere die Kette für die Helix
            start = int(line[21:25].strip())
            end = int(line[33:37].strip())
            for i in range(start, end + 1):
                ss_info[(chain, i)] = 'H'  # Speichere Helix-Info mit Kette und Position
        elif line.startswith('SHEET'):
            chain = line[21]  # Extrahiere die Kette für das Sheet
            start = int(line[22:26].strip())
            end = int(line[33:37].strip())
            for i in range(start, end + 1):
                ss_info[(chain, i)] = 'E'  # Speichere Sheet-Info mit Kette und Position
    return ss_info



def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description="Parse PDB file and extract secondary structure elements")
    parser.add_argument("pdb_id", help="PDB ID to process")
    parser.add_argument("atom_type", help="Atom type to extract")
    args = parser.parse_args()

    # PDB-Datei herunterladen
    pdb_data = download_pdb(args.pdb_id)


if __name__ == "__main__":
    main()
