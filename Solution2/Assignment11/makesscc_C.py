#!/usr/bin/env python3

import argparse
import math
import sys
import requests

def download_pdb(pdb_id):
    """
    Lädt die PDB-Datei basierend auf der gegebenen PDB-ID herunter.
    """
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb" # URL für den Download der PDB-Datei
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download PDB file for ID {pdb_id}")


def parse_pdb(atom_type):
    """Read and parse PDB data from stdin, ensuring no relevant information is missed."""
    atoms = []
    model_started = False
    for line in sys.stdin:
        if line.strip() == '' or line.startswith('REMARK'):
            continue  # Ignoriere leere Zeilen und Kommentare
        if line.startswith('MODEL'):
            if model_started:
                break  # Beende das Einlesen nach dem ersten Modell
            model_started = True
            continue
        if line.startswith('ENDMDL'):
            break
        if line.startswith('ATOM') and line[12:16].strip() == atom_type:
            # Extrahiere relevante Informationen korrekt
            chain = line[21]
            pos = int(line[22:26].strip())
            serial = int(line[6:11].strip())
            aa = line[17:20].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            atoms.append((chain, pos, serial, aa, x, y, z))
    return atoms


def calculate_distance(atom1, atom2):
    """Calculate the Euclidean distance between two atoms."""
    return math.sqrt((atom1[4] - atom2[4])**2 + (atom1[5] - atom2[5])**2 + (atom1[6] - atom2[6])**2)

def calculate_contacts(atoms, distance_threshold, length_threshold):
    """Calculate global and local contacts between atoms."""
    contacts = []
    for i, atom1 in enumerate(atoms):
        global_contacts = 0
        local_contacts = 0
        for j, atom2 in enumerate(atoms):
            if i != j:
                distance = calculate_distance(atom1, atom2)
                if distance < distance_threshold:
                    if abs(atom1[1] - atom2[1]) < length_threshold:
                        local_contacts += 1
                    else:
                        global_contacts += 1
        contacts.append((atom1[0], atom1[1], atom1[2], atom1[3], 'NA', global_contacts, local_contacts))
    return contacts

def print_sscc_table(contacts):
    """Print the .sscc table."""
    print("chain\tpos\tserial\taa\tss\tglobal\tlocal")
    for contact in contacts:
        print(f"{contact[0]}\t{contact[1]}\t{contact[2]}\t{contact[3]}\t{contact[4]}\t{contact[5]}\t{contact[6]}")


def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="PDB ID")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")

    args = parser.parse_args()

    # Verarbeitung der PDB-Daten von stdin
    atoms = parse_pdb(args.type)
    contacts = calculate_contacts(atoms, args.distance, args.length)
    print_sscc_table(contacts)

if __name__ == "__main__":
    main()