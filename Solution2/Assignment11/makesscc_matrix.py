#!/usr/bin/env python3

import argparse
import math
import requests
import numpy as np


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
    ss_info = {} #
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
            aa = aa_dict.get(line[17:20].strip().upper(), 'X')  # Benutze das Dictionary
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            ss = ss_info.get((chain, pos), 'C')  # Verwende Tupel aus Kette und Position als Schlüssel
            atoms.append((chain, pos, serial, aa, x, y, z, ss))
    return atoms



def calculate_distance(atom1, atom2):
    # Calculate the Euclidean distance between two atoms.
    return math.sqrt((atom1[4] - atom2[4])**2 + (atom1[5] - atom2[5])**2 + (atom1[6] - atom2[6])**2)


def calculate_contacts(atoms, distance_threshold, length_threshold):
    contacts = []
    for i, atom1 in enumerate(atoms):
        global_contacts = 0
        local_contacts = 0
        for j, atom2 in enumerate(atoms):
            if i != j:
                # Überprüfe, ob die Atome zur selben Kette gehören
                same_chain = atom1[0] == atom2[0]

                distance = calculate_distance(atom1, atom2)
                if distance < distance_threshold:
                    # Überprüfe, ob der Kontakt lokal ist (basierend auf Sequenzdistanz und gleicher Kette)
                    if abs(atom1[1] - atom2[1]) < length_threshold and same_chain:
                        local_contacts += 1
                    else:
                        global_contacts += 1
        contacts.append((atom1[0], atom1[1], atom1[2], atom1[3], atom1[7], global_contacts, local_contacts))
    return contacts


def print_sscc_table(contacts):
    # Print the .sscc table.
    output = ["chain\tpos\tserial\taa\tss\tglobal\tlocal"]
    for contact in contacts:
        output.append(f"{contact[0]}\t{contact[1]}\t{contact[2]}\t{contact[3]}\t{contact[4]}\t{contact[5]}\t{contact[6]}")

    print("\n".join(output))


def create_contact_matrix(atoms, distance_threshold, length_threshold):
    # Stelle sicher, dass wir eine korrekte Anzahl von Atomen haben
    if len(atoms) == 0:
        return np.array([], dtype=int).reshape(0, 0)  # Leere 2D-Matrix für den Fall, dass keine Atome vorhanden sind

    size = len(atoms) # size = Anzahl der Atome
    matrix = np.zeros((size, size), dtype=int) # numpy array mit 0en, size x size

    for i in range(size): # range von 0 bis size
        for j in range(i + 1, size):
            distance = calculate_distance(atoms[i], atoms[j])
            # Überprüfe die Distanz und, ob es sich nicht um denselben Atom handelt
            if distance < distance_threshold and abs(atoms[i][1] - atoms[j][1]) >= length_threshold:
                matrix[i][j] = 1
                matrix[j][i] = 1

    return matrix


def save_matrix_to_file(matrix, file_path):
    if matrix.ndim != 2:
        raise ValueError("Die übergebene Matrix ist nicht 2-dimensional.")

    # Speichere die Matrix als Textdatei, Trennzeichen ist ein Leerzeichen
    np.savetxt(file_path, matrix, fmt='%d', delimiter=' ')

def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="PDB ID")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")
    parser.add_argument('--contactmatrix', type=str, help="Zielpfad für die Speicherung der Kontaktmatrix-Datei")

    args = parser.parse_args()

    # Lese PDB-Daten einmalig ein
    pdb_data = download_pdb(args.id)

    # Verarbeite die PDB-Daten
    ss_info = parse_secondary_structure(pdb_data)
    atoms = parse_pdb(pdb_data, args.type, ss_info)

    # Erzeuge und speichere die Kontaktmatrix, falls gewünscht
    if args.contactmatrix:
        contact_matrix = create_contact_matrix(atoms, args.distance, args.length)
        save_matrix_to_file(contact_matrix, args.contactmatrix)
        print(f"Kontaktmatrix gespeichert unter: {args.contactmatrix}")
    else:
        contacts = calculate_contacts(atoms, args.distance, args.length)
        print_sscc_table(contacts)

if __name__ == "__main__":
    main()
