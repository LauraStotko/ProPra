#!/usr/bin/env python3

import argparse
import requests

aa_dict = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLU": "E",
    "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
    "TYR": "Y", "VAL": "V"
}

def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download PDB file for ID {pdb_id}")

def parse_secondary_structure(pdb_data):
    ss_info = {}
    for line in pdb_data.splitlines():
        if line.startswith('HELIX'):
            chain = line[19]
            start = int(line[21:25].strip())
            end = int(line[33:37].strip())
            for i in range(start, end + 1):
                ss_info[(chain, i)] = 'H'
        elif line.startswith('SHEET'):
            chain = line[21]
            start = int(line[22:26].strip())
            end = int(line[33:37].strip())
            for i in range(start, end + 1):
                ss_info[(chain, i)] = 'E'
    return ss_info

def parse_pdb(pdb_data, atom_type, ss_info):
    atoms = []
    for line in pdb_data.splitlines():
        if line.startswith('ATOM') and line[12:16].strip() == atom_type:
            chain = line[21]
            pos = int(line[22:26].strip())
            aa = aa_dict.get(line[17:20].strip().upper(), 'X')
            ss = ss_info.get((chain, pos), 'C')
            atoms.append((chain, aa, ss))
    return atoms


def read_ids_from_file(file_path):
    import re

    # RegEx für eine typische PDB-ID, angepasst nach Bedarf
    # Dieses Beispiel nimmt an, dass eine PDB-ID aus 4 alphanumerischen Zeichen besteht
    pdb_id_pattern = re.compile(r'\b[a-zA-Z0-9]{4}\b')

    pdb_ids = set()  # Verwendung eines Sets zur Vermeidung von Duplikaten

    with open(file_path, 'r') as file:
        for line in file:
            # Findet alle PDB-IDs in der Zeile gemäß dem definierten Muster
            found_ids = pdb_id_pattern.findall(line)
            # Fügt gefundene IDs dem Set hinzu, Duplikate werden automatisch entfernt
            pdb_ids.update(found_ids)

    return list(pdb_ids)  # Konvertiert das Set zurück in eine Liste für die Ausgabe



def write_seclib_file(pdb_id, chains_data, f):
    for chain_id, chain_data in chains_data.items():
        if 'AA' in chain_data and 'SS' in chain_data and len(chain_data['AA']) == len(chain_data['SS']):
            f.write(f">{pdb_id}_{chain_id}\n")
            f.write("AS " + "".join(chain_data['AA']) + "\n")
            f.write("SS " + "".join(chain_data['SS']) + "\n")


def extract_sequences_and_structures(atoms, ss_info):
    chains_data = {}
    for chain, aa, ss in atoms:
        if chain not in chains_data:
            chains_data[chain] = {'AA': [], 'SS': []}
        chains_data[chain]['AA'].append(aa)
        chains_data[chain]['SS'].append(ss)
    return chains_data


def main():
    parser = argparse.ArgumentParser(description="Erzeugt Seclib-Dateien aus PDB- oder DSSP-Daten.")
    parser.add_argument('--ids', nargs='*', help="Liste von PDB-IDs oder DSSP-Dateinamen", default=[])
    parser.add_argument('--id_file', type=str, help="Pfad zu einer Textdatei mit PDB-IDs oder DSSP-Dateinamen")
    parser.add_argument('--output', type=str, required=True, help="Dateipfad für die gesammelte Ausgabe-Seclib-Datei")
    parser.add_argument('--atom_type', type=str, default="CA", help="Atomtyp für PDB Parsing (Standard: CA)")

    args = parser.parse_args()

    ids = args.ids if args.ids else read_ids_from_file(args.id_file) if args.id_file else []

    if not ids:
        print("Keine PDB-IDs oder DSSP-Dateinamen angegeben.")
        return

    with open(args.output, 'w') as f:
        for pdb_id in ids:
            try:
                pdb_data = download_pdb(pdb_id)
                ss_info = parse_secondary_structure(pdb_data)
                atoms = parse_pdb(pdb_data, args.atom_type, ss_info)
                chains_data = extract_sequences_and_structures(atoms, ss_info)
                write_seclib_file(pdb_id, chains_data, f)
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten bei der Verarbeitung von {pdb_id}: {e}. Überspringe...")
                f.write(f"# Fehler bei der Verarbeitung von {pdb_id}: Übersprungen wegen eines Fehlers\n")
                continue


if __name__ == "__main__":
    main()



