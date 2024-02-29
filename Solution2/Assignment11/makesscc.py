#!/usr/bin/env python3

import argparse
import requests
import matplotlib.pyplot as plt
import numpy as np
import csv

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

def parse_pdb(pdb_content, atom_type):
    atoms = []  # Initialisierung einer leeren Liste für die Atominformationen
    model_started = False  # Flag, um zu überprüfen, ob das erste Modell bereits begonnen hat
    for line in pdb_content.splitlines():
        if line.startswith('MODEL'):
            if model_started:  # Wenn das erste Modell bereits begonnen hat, brechen wir die Schleife ab
                break
            else:
                model_started = True  # Markieren, dass das erste Modell begonnen hat
        elif line.startswith('ENDMDL'):
            break  # Beendet die Schleife nach dem ersten Modell
        elif line.startswith('ATOM'):  # Wenn die Zeile mit 'ATOM' beginnt, handelt es sich um eine Atominformation
            chain = line[21]  # Extrahierung der Ketteninformation
            pos = int(line[22:26].strip())  # Extrahierung der Positionsinformation
            serial = int(line[6:11].strip())  # Extrahierung der Seriennummer
            aa = line[17:20].strip()  # Extrahierung der Aminosäureinformation
            atom = line[12:16].strip()  # Extrahierung des Atomtyps

            if atom == atom_type:  # Wenn der Atomtyp dem gesuchten Atomtyp entspricht, wird die Atominformation gespeichert
                atom_info = {
                    'chain': chain,
                    'pos': pos,
                    'serial': serial,
                    'aa': aa,
                    'atom': atom,
                    'x': float(line[30:38].strip()),
                    'y': float(line[38:46].strip()),
                    'z': float(line[46:54].strip())
                }
                atoms.append(atom_info)
    return atoms


# Funktion zur Berechnung der Distanz zwischen zwei Atomen
def calculate_distance(atom1, atom2):
    x1, y1, z1 = atom1['x'], atom1['y'], atom1['z']
    x2, y2, z2 = atom2['x'], atom2['y'], atom2['z']
    # Berechnung der euklidischen Distanz
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    return distance

# Funktion zur Identifizierung von Kontakten und Erstellung der Kontaktmatrix
def identify_contacts_and_create_matrix(atoms, distance_threshold, sequence_distance):
    num_atoms = len(atoms) # Anzahl der Atome
    contact_matrix = [[0 for _ in range(num_atoms)] for _ in range(num_atoms)] # Initialisierung der Kontaktmatrix
    contact_info = [{'global': 0, 'local': 0} for _ in range(num_atoms)] # Initialisierung der Kontaktinformationen

    # Iteration über alle Atome und Berechnung der Distanz zu allen anderen Atomen
    for i in range(num_atoms):
        for j in range(i + 1, num_atoms):
            distance = calculate_distance(atoms[i], atoms[j])
            if distance <= distance_threshold: # Wenn die Distanz kleiner oder gleich der Schwellendistanz ist, handelt es sich um einen Kontakt
                contact_matrix[i][j] = 1
                contact_matrix[j][i] = 1

                # Unterscheidung zwischen lokalen und globalen Kontakten
                if abs(atoms[i]['pos'] - atoms[j]['pos']) < sequence_distance:
                    contact_info[i]['local'] += 1
                    contact_info[j]['local'] += 1
                else: # Wenn die Sequenzdistanz größer ist, handelt es sich um einen globalen Kontakt
                    contact_info[i]['global'] += 1
                    contact_info[j]['global'] += 1

    return contact_matrix, contact_info

# Funktion zum Speichern der .sscc Datei
def save_sscc_file(contact_info, file_path):
    with open(file_path, 'w') as file:
        file.write("chain\tpos\tserial\taa\tss\tglobal\tlocal\n")
        for info in contact_info:
            # Verwenden von get() mit einem Standardwert, um KeyError zu vermeiden
            chain = info.get('chain', 'Unbekannt')
            pos = info.get('pos', 'Unbekannt')
            serial = info.get('serial', 'Unbekannt')
            aa = info.get('aa', 'Unbekannt')
            ss = 'Unbekannt'  # Da 'ss' (Sekundärstruktur) nicht aus 'info' extrahiert wird
            global_contacts = info.get('global', 0)
            local_contacts = info.get('local', 0)

            line = f"{chain}\t{pos}\t{serial}\t{aa}\t{ss}\t{global_contacts}\t{local_contacts}\n"
            file.write(line)


# Funktion zur Visualisierung der Kontaktmatrix
def visualize_contact_matrix(contact_matrix, image_path):
    matrix = np.array(contact_matrix) # Konvertierung der Kontaktmatrix in ein Numpy-Array
    plt.imshow(matrix, cmap='viridis', interpolation='none') # Erstellung der Visualisierung
    plt.colorbar(label='Kontakt (1 = Kontakt, 0 = kein Kontakt)')
    plt.title('Kontaktmatrix')
    plt.xlabel('Aminosäure Index')
    plt.ylabel('Aminosäure Index')
    plt.savefig(image_path)
    plt.show()
    # plt.close()

def save_contact_matrix_csv(contact_matrix, csv_path):
    """
    Speichert die Kontaktmatrix in einer CSV-Datei.
    """
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in contact_matrix:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="PDB ID")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")
    parser.add_argument('--contactmatrix', type=str, help="Pfad zur Speicherung der Kontaktmatrix-Visualisierung")
    parser.add_argument('--ssccfile', type=str, required=False, help="Pfad zur Speicherung der .sscc Datei")

    args = parser.parse_args()

    # Extrahieren und Verarbeiten der PDB-Daten
    pdb_content = download_pdb(args.id)
    atoms = parse_pdb(pdb_content, args.type)
    contact_matrix, contact_info = identify_contacts_and_create_matrix(atoms, args.distance, args.length)

    # Visualisierung der Kontaktmatrix, wenn ein Pfad angegeben wurde
    if args.contactmatrix:
        visualize_contact_matrix(contact_matrix, args.contactmatrix)

    # Speichern der .sscc Datei, wenn ein Pfad angegeben wurde
    if args.ssccfile:
        save_sscc_file(contact_info, args.ssccfile)

if __name__ == "__main__":
    main()