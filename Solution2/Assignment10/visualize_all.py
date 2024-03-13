#!/usr/bin/env python

import argparse
import os
import urllib.request
import math
# from get_pdb import download_pdb
# from visualize_mol import visualize_mol

def download_pdb(id):
    url = f"https://files.rcsb.org/view/{id}.pdb"
    try:
        pdb = urllib.request.urlopen(url)
        if pdb.getcode() == 200:
            return pdb.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print(f"Sorry, this PDB ID {id} does not exist")
        return None

def download_as_fasta(id):
    url = f"https://www.rcsb.org/fasta/entry/{id}/display"
    try:
        fasta = urllib.request.urlopen(url)
        if fasta.getcode() == 200:
            return fasta.read().decode('utf-8')
    except urllib.request.HTTPError as e:
        print(f"Sorry, this PDB ID {id} does not exist")
        return None

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


def calculate_secondary_structure_proportion(ss_info, pdb_data): # Anteil der Aminosäuren, die zu Sekundärstrukturen gehören
    # Calculate the proportion of amino acids belonging to secondary structures.
    aa_count = sum(1 for line in pdb_data.splitlines() if line.startswith('ATOM') and line[13:15].strip() == 'CA')
    ss_count = len(ss_info)
    proportion = ss_count / aa_count if aa_count > 0 else 0
    return proportion


def parse_pdb_for_extreme_coordinates(pdb_file_path):
    #  Parse the PDB file to find extreme coordinates of all atoms to define the smallest box.
    with open(pdb_file_path, 'r') as file:
        coords = [line for line in file if line.startswith("ATOM")] # speichert alle Zeilen, die mit ATOM beginnen
        if not coords:
            return None

        # speichert die x-, y- und z-Koordinaten in separate Listen
        x_coords = [float(line.split()[6]) for line in coords]
        y_coords = [float(line.split()[7]) for line in coords]
        z_coords = [float(line.split()[8]) for line in coords]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        min_z, max_z = min(z_coords), max(z_coords)

        return min_x, max_x, min_y, max_y, min_z, max_z


def calculate_box_size(min_x, max_x, min_y, max_y, min_z, max_z):
    # Calculate the size of the smallest axis-aligned box that the protein can fit into.
    return max_x - min_x, max_y - min_y, max_z - min_z


# Berechnung des euklidischen Abstands
def calculate_distance(coord1, coord2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)))


# Extraktion der Cα-Koordinaten
def extract_ca_coordinates(pdb_data):
    # extrahieren von ca koordinaten
    ca_coords = [(line[30:38].strip(), line[38:46].strip(), line[46:54].strip())
                 for line in pdb_data.splitlines() if line.startswith("ATOM") and " CA " in line]
    # speichern der ersten und letzten ca koordinaten
    if ca_coords:
        first_ca = tuple(map(float, ca_coords[0]))
        last_ca = tuple(map(float, ca_coords[-1]))
        return first_ca, last_ca
    return None, None

def calculate_volume(box_size):
    # Berechnet das Volumen der Box
    return box_size[0] * box_size[1] * box_size[2]

def extract_cb_coordinates(pdb_data):
    # Extrahiert Cβ-Koordinaten, außer für Glycin (Glycin hat kein Cβ)
    cb_coords = {}
    for line in pdb_data.splitlines():
        if line.startswith("ATOM") and line[13:15] == "CB":
            residue_id = line[22:26].strip()
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            cb_coords[residue_id] = (x, y, z)
    return cb_coords

"""
def main():
    parser = argparse.ArgumentParser(description="Download PDB files and analyze structures.")
    parser.add_argument("--id", nargs="+", required=True, help="List of PDB IDs to process.")
    parser.add_argument("--output", default=".", help="Directory to save PDB files and analysis.")
    args = parser.parse_args()


    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    for pdb_id in args.id:
        pdb_data = download_pdb(pdb_id)
        if pdb_data is None:
            continue

        pdb_file_path = f'{output_dir}/{pdb_id}.pdb'
        with open(pdb_file_path, 'w') as pdb_file:
            pdb_file.write(pdb_data)

        # After analysis, visualize the molecule
        visualize_mol(pdb_id, colourized=True, html=True, output_path=output_dir)

    # visualize mol

    for pdb_id in args.id:
        pdb_data = download_pdb(pdb_id)
        if pdb_data is None:
            continue

        pdb_file_path = f'{output_dir}/{pdb_id}.pdb'
        with open(pdb_file_path, 'w') as pdb_file:
            pdb_file.write(pdb_data)

    first_ca, last_ca = extract_ca_coordinates(pdb_data)
        if first_ca and last_ca:
            distance = calculate_distance(first_ca, last_ca)
            print(f"Abstand zwischen den Cα-Atomen der ersten und letzten Aminosäure in {pdb_id}: {distance:.2f} Å")

        extreme_coords = parse_pdb_for_extreme_coordinates(pdb_data)
        if extreme_coords:
            box_size = calculate_box_size(*extreme_coords)
            print(
                f"Größe der kleinsten achsenparallelen Box für {pdb_id}: {box_size[0]:.2f} x {box_size[1]:.2f} x {box_size[2]:.2f} Å")
        else:
            print(f"Keine Atomkoordinaten gefunden in {pdb_id}.")
"""


def main():
    parser = argparse.ArgumentParser(description="Download PDB files and analyze structures.")
    parser.add_argument("--id", nargs="+", required=True, help="List of PDB IDs to process.")
    parser.add_argument("--output", default=".", help="Directory to save PDB files and analysis.")
    parser.add_argument("--fasta", action='store_true', help="Download and save as FASTA format.")
    args = parser.parse_args()

    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdb_id in args.id:
        pdb_data = download_pdb(pdb_id)
        if pdb_data is None:
            continue

        analysis_file_path = f'{output_dir}/{pdb_id}_analysis.txt'
        with open(analysis_file_path, 'w') as analysis_file:

            if args.fasta:
                fasta_data = download_as_fasta(pdb_id)
                if fasta_data:
                    fasta_file_path = f'{output_dir}/{pdb_id}.fasta'
                    with open(fasta_file_path, 'w') as fasta_file:
                        fasta_file.write(fasta_data)
                    analysis_file.write(f"FASTA data saved for {pdb_id}\n")
                else:
                    analysis_file.write(f"Failed to download FASTA data for {pdb_id}\n")

            ss_info = parse_secondary_structure(pdb_data)
            proportion = calculate_secondary_structure_proportion(ss_info, pdb_data)
            analysis_file.write(f"Proportion of amino acids in secondary structures for {pdb_id}: {proportion:.4f}\n")

            cb_coords = extract_cb_coordinates(pdb_data)
            analysis_file.write(f"Number of Cβ atoms found: {len(cb_coords)}\n")

            first_ca, last_ca = extract_ca_coordinates(pdb_data)
            if first_ca and last_ca:
                distance = calculate_distance(first_ca, last_ca)
                analysis_file.write(f"Distance between the Cα atoms of the first and last amino acid in {pdb_id}: {distance:.4f} Å\n")

            extreme_coords = parse_pdb_for_extreme_coordinates(pdb_data)
            if extreme_coords:
                box_size = calculate_box_size(*extreme_coords)
                volume = calculate_volume(box_size)
                analysis_file.write(f"Box dimensions for {pdb_id}: X={box_size[0]:.4f} Å, Y={box_size[1]:.4f} Å, Z={box_size[2]:.4f} Å\n")
                analysis_file.write(f"Volume of the smallest axis-aligned box for {pdb_id}: {volume:.4f} Å³\n")
            else:
                analysis_file.write(f"No atom coordinates found in {pdb_id}.\n")

if __name__ == "__main__":
    main()

