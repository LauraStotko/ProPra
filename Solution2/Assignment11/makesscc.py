#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np


# Funktion zum Einlesen und Parsen der PDB-Datei
def parse_pdb(file_path, atom_type):
    atoms = [] # Initialisierung einer leeren Liste für die Atominformationen
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('ATOM'): # Wenn die Zeile mit 'ATOM' beginnt, handelt es sich um eine Atominformation
                chain = line[21] # Extrahierung der Ketteninformation
                pos = int(line[22:26].strip()) # Extrahierung der Positionsinformation
                serial = int(line[6:11].strip()) # Extrahierung der Seriennummer
                aa = line[17:20].strip() # Extrahierung der Aminosäureinformation
                atom = line[12:16].strip() # Extrahierung des Atomtyps

                if atom == atom_type: # Wenn der Atomtyp dem gesuchten Atomtyp entspricht, wird die Atominformation gespeichert
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

# Funktion zum Speichern der Kontaktmatrix als CSV-Datei
"""
def save_contact_matrix_csv(contact_matrix, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(contact_matrix)
"""


# Funktion zum Speichern der .sscc Datei
def save_sscc_file(contact_info, file_path): # Speichert die Kontaktinformationen in einer .sscc Datei
    with open(file_path, 'w') as file:
        # Schreiben der Headerzeile
        file.write("chain\tpos\tserial\taa\tss\tglobal\tlocal\n")
        for info in contact_info: # Schreiben der Kontaktinformationen für jedes Atom
            line = f"{info['chain']}\t{info['pos']}\t{info['serial']}\t{info['aa']}\t'Unbekannt'\t{info['global']}\t{info['local']}\n"
            file.write(line) # Schreiben der Zeile in die Datei


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


def main():
    parser = argparse.ArgumentParser(description="Erzeugt eine Contact Number Datei (*.sscc) für eine gegebene PDB ID.")
    parser.add_argument('--id', type=str, required=True, help="Pfad zur PDB-Datei")
    parser.add_argument('--distance', type=float, required=True, help="Kontaktdistanz")
    parser.add_argument('--type', type=str, required=True, help="Atomtyp")
    parser.add_argument('--length', type=int, required=True, help="Sequenzdistanz für lokale Kontakte")
    parser.add_argument('--contactmatrix', type=str, help="Pfad zur Speicherung der Kontaktmatrix-Visualisierung")

    args = parser.parse_args()

    atoms = parse_pdb(args.id, args.type)
    contact_matrix, contact_info = identify_contacts_and_create_matrix(atoms, args.distance, args.length)

    if args.contactmatrix: # Wenn ein Pfad zur Speicherung der Kontaktmatrix-Visualisierung angegeben wurde, wird die Visualisierung erstellt
        visualize_contact_matrix(contact_matrix, args.contactmatrix)

    # Beispiel für Speicherort der .sscc Datei, kann angepasst werden
    # save_sscc_file(contact_info, "protein_contacts.sscc")


if __name__ == "__main__":
    main()