#!/usr/bin/env python3
import argparse
import requests
import os

def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        print(f"Warning: Failed to download PDB file for ID {pdb_id}. Skipping...")
        return None

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
    aa_dict = {
        "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLU": "E",
        "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
        "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
        "TYR": "Y", "VAL": "V"
    }
    atoms = []
    for line in pdb_data.splitlines():
        if line.startswith('ATOM') and line[12:16].strip() == atom_type:
            chain = line[21]
            pos = int(line[22:26].strip())
            serial = int(line[6:11].strip())
            aa = aa_dict.get(line[17:20].strip().upper(), 'X')
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            ss = ss_info.get((chain, pos), 'C')
            atoms.append((chain, pos, serial, aa, x, y, z, ss))
    return atoms

def read_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split() for line in file if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Download and process PDB files to generate a single seclib file.")
    parser.add_argument('--id_file', type=str, required=True, help="File containing PDB IDs")
    parser.add_argument('--output', type=str, required=True, help="Output seclib file")
    parser.add_argument('--atom_type', type=str, default="CA", help="Atom type for PDB parsing (default: CA)")
    args = parser.parse_args()

    pdb_ids = read_ids_from_file(args.id_file)
    with open(args.output, 'w') as output_file:
        for pdb_pair in pdb_ids:
            for pdb_id in pdb_pair:
                pdb_data = download_pdb(pdb_id)
                if not pdb_data:
                    continue  # Überspringt die aktuelle ID, wenn der Download fehlschlägt

                ss_info = parse_secondary_structure(pdb_data)
                atoms = parse_pdb(pdb_data, args.atom_type, ss_info)
                for atom in atoms:
                    chain, pos, serial, aa, x, y, z, ss = atom
                    output_file.write(f"{pdb_id}_{chain}:{pos} {aa} {ss}\n")

if __name__ == "__main__":
    main()


