#!/usr/bin/env python3

import argparse
import requests
import os


def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download PDB file for ID {pdb_id}")

def download_dssp(dssp_id):
    url = f"https://files.rcsb.org/download/{dssp_id}.dssp"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download DSSP file for ID {dssp_id}")


def read_ids_from_file(file_path):
    """Liest IDs aus einer Datei und gibt sie als Liste zurück."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def read_dssp_file(dssp_file_path):
    secondary_structure = {}
    with open(dssp_file_path, 'r') as file:
        start_reading = False
        for line in file:
            if start_reading:
                if len(line) > 13:
                    chain_id = line[11]
                    residue_number = line[5:10].strip()
                    dssp_code = line[16]
                    if chain_id not in secondary_structure:
                        secondary_structure[chain_id] = []
                    secondary_structure[chain_id].append((residue_number, dssp_code))
            elif line.startswith("  #  RESIDUE AA STRUCTURE"):
                start_reading = True
    return secondary_structure


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


def parse_dssp(dssp_file_path):
    chains_data = {}
    start_parsing = False

    with open(dssp_file_path, 'r') as file:
        for line in file:
            if '  #  RESIDUE AA STRUCTURE' in line:
                start_parsing = True
                continue
            if start_parsing and len(line) > 13:
                chain = line[11]
                aa = aa_dict.get(line[13], 'X')  # Verwende das Dictionary für Aminosäure-Abkürzungen
                ss = line[16]

                if chain not in chains_data:
                    chains_data[chain] = {'AA': [], 'SS': []}

                chains_data[chain]['AA'].append(aa)
                if ss in ['H', 'G', 'I']:  # Helix
                    chains_data[chain]['SS'].append('H')
                elif ss in ['E', 'B']:     # Sheet
                    chains_data[chain]['SS'].append('E')
                else:                      # Coil
                    chains_data[chain]['SS'].append('C')

    return chains_data


def write_seclib_file(pdb_id, chains_data, file):
    for chain_id, chain_data in chains_data.items():
        if 'AA' in chain_data and 'SS' in chain_data and len(chain_data['AA']) == len(chain_data['SS']):
            file.write(f">{pdb_id}_{chain_id}\n")
            file.write("AS " + "".join(chain_data['AA']) + "\n")
            file.write("SS " + "".join(chain_data['SS']) + "\n")
        else:
            print(f"Fehler in den Daten für {pdb_id}_{chain_id}: Ungültige Datenstruktur oder inkonsistente Längen")



def main():
    parser = argparse.ArgumentParser(description="Verarbeitet IDs standardmäßig als PDB, bei Fehlschlag als DSSP.")
    parser.add_argument('--ids', nargs='+', help="Liste von IDs ohne spezifischen Typ")
    parser.add_argument('--id_file', type=str, help="Pfad zu einer Datei mit IDs, eine ID pro Zeile")
    parser.add_argument('--output_file', type=str, required=True, help="Name der Ausgabe-Seclib-Datei")

    args = parser.parse_args()

    if args.id_file:
        ids = read_ids_from_file(args.id_file)
    else:
        ids = args.ids

    with open(args.output_file, 'w') as file:
        for file_id in ids:
            try:
                pdb_data = download_pdb(file_id)
                if pdb_data:
                    ss_info = parse_secondary_structure(pdb_data)
                    atoms = parse_pdb(pdb_data, "CA", ss_info)
                    chains_data = {}
                    for atom in atoms:
                        chain = atom[0]
                        if chain not in chains_data:
                            chains_data[chain] = {'AA': [], 'SS': []}
                        chains_data[chain]['AA'].append(atom[3])
                        chains_data[chain]['SS'].append(atom[7])
                    write_seclib_file(file_id, chains_data, file)
                else:
                    raise Exception("PDB data not found, attempting DSSP.")
            except Exception as pdb_error:
                try:
                    dssp_file_path = download_dssp(file_id)
                    chains_data = parse_dssp(dssp_file_path)
                    write_seclib_file(file_id, chains_data, file)
                except Exception as dssp_error:
                    print(f"Failed to process {file_id} as both PDB and DSSP: {dssp_error}")


if __name__ == "__main__":
    main()

