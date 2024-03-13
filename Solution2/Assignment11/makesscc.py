#!/usr/bin/env python3

import argparse
import math
import requests # modul für http requests


def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url) # Führe den HTTP-Request aus
    if response.status_code == 200: # 200 ist der Code für eine erfolgreiche Anfrage
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

def parse_secondary_structure(pdb_data): # Analyse der Sekundärstruktur
    ss_info = {} # Initialisiert ein leeres Dictionary
    for line in pdb_data.splitlines(): # Iteriere über jede Zeile der PDB-Datei
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


# Extrahiert spezifische Atomdaten aus den PDB-Daten basierend auf einem gegebenen Atomtyp.
def parse_pdb(pdb_data, atom_type, ss_info): # ss_info ist das Dictionary aus parse_secondary_structure
    atoms = [] # Initialisiere eine leere Liste
    model_started = False # Initialisiere eine Variable, um zu überprüfen, ob das Modell begonnen hat
    for line in pdb_data.splitlines(): # splitlines() teilt die Zeichenkette in Zeilen auf
        if line.strip() == '' or line.startswith('REMARK'): # strip() entfernt Leerzeichen am Anfang und Ende der Zeichenkette
            continue
        elif line.startswith('MODEL') and not model_started:
            model_started = True # parsing der Atome beginnt
            continue
        elif line.startswith('ENDMDL'): # Wenn das Ende des Modells erreicht ist,
            break
        # extrahiert wichtige Informationen aus der Zeile
        elif line.startswith('ATOM') and line[12:16].strip() == atom_type: # 12:16 Position für Atommtyp
            chain = line[21] # Extrahiere die Kette des Atoms
            pos = int(line[22:26].strip()) # Positionsnummer der Aminosäure innerhalb des Atoms zum zuordnen
            serial = int(line[6:11].strip()) # eindeutige Seriennummer des Atoms
            aa = aa_dict.get(line[17:20].strip().upper(), 'X')  # Benutze das Dictionary
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            ss = ss_info.get((chain, pos), 'C')  # nimmt info pber H und S aus ss-info, wenn kein Schlüssel C als default
            atoms.append((chain, pos, serial, aa, x, y, z, ss)) # fügt der Atoms liste ein tupel mit informationen hinzu
    return atoms



def calculate_distance(atom1, atom2): # Distanz berechnen zum berechnen von Kontakten
    # Calculate the Euclidean distance between two atoms.
    # summiert die quadrierten Differenzen der x-, y- und z-Koordinaten
    return math.sqrt((atom1[4] - atom2[4])**2 + (atom1[5] - atom2[5])**2 + (atom1[6] - atom2[6])**2)
    # (atom1[4] - atom2[4])**2: Berechnet das Quadrat der Differenz zwischen den x-Koordinaten der beiden Atome.
    # (atom1[5] - atom2[5])**2: -"- y-Koordinaten



def calculate_contacts(atoms, distance_threshold, length_threshold):
    contacts = [] # Liste
    for i, atom1 in enumerate(atoms): # Loop über atoms, i Index, atom1 Atom an der aktuellen Position
        global_contacts = 0
        local_contacts = 0
        for j, atom2 in enumerate(atoms): # zweite Schleife um atom1 mit atom2 zu vergleichen
            if i != j: # Teste dass atom1 und atom2 nicht das selbe Atom sind
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


def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="PDB ID")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")

    args = parser.parse_args()

    # Lese PDB-Daten einmalig ein
    pdb_data = download_pdb(args.id)

    # Verarbeite die PDB-Daten
    ss_info = parse_secondary_structure(pdb_data)
    atoms = parse_pdb(pdb_data, args.type, ss_info)
    contacts = calculate_contacts(atoms, args.distance, args.length)
    print_sscc_table(contacts) # sscc: secondary structure contact count

if __name__ == "__main__":
    main()
