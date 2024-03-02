#!/usr/bin/env python3

import argparse
import math
import requests
import numpy as np
import matplotlib.pyplot as plt


def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download PDB file for ID {pdb_id}")


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
    model_started = False
    for line in pdb_data.splitlines():
        if line.strip() == '' or line.startswith('REMARK'):
            continue
        if line.startswith('MODEL') and not model_started:
            model_started = True
            continue
        if line.startswith('ENDMDL'):
            break
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


def calculate_distance(atom1, atom2):
    return math.sqrt((atom1[4] - atom2[4])**2 + (atom1[5] - atom2[5])**2 + (atom1[6] - atom2[6])**2)


def generate_contact_matrix(atoms, distance_threshold):
    n = len(atoms)
    c = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            if calculate_distance(atoms[i], atoms[j]) < distance_threshold:
                c[i, j] = c[j, i] = 1
    return c


def plot_heatmap(c, file_name):
    plt.figure(figsize=(10, 8))
    plt.imshow(c, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.savefig(file_name)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="PDB ID")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")

    args = parser.parse_args()

    pdb_data = download_pdb(args.id)
    ss_info = parse_secondary_structure(pdb_data)
    atoms = parse_pdb(pdb_data, args.type, ss_info)
    c = generate_contact_matrix(atoms, args.distance)
    np.savetxt(f"{args.id}_contact_matrix.csv", c, delimiter=",")
    plot_heatmap(c, f"{args.id}_heatmap.png")


if __name__ == "__main__":
    main()
