import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle

# Dictionary für Aminosäure-Abkürzungen
aa_dict = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLU": "E",
    "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
    "TYR": "Y", "VAL": "V"
}

# Eindeutige Werte für Sekundärstrukturen
structures = ['H', 'E', 'C']

# Initialisierung der Encoder
aa_encoder = LabelEncoder()
aa_encoder.fit(list(aa_dict.values()))
structure_encoder = LabelEncoder()
structure_encoder.fit(structures)

# One-Hot-Encoding für Aminosäuren
aa_onehot_encoder = OneHotEncoder(sparse=False)
aa_onehot_encoded = aa_onehot_encoder.fit_transform(aa_encoder.transform(list(aa_dict.values())).reshape(-1, 1))

def encode_sequence(sequence, encoder=aa_encoder, onehot_encoder=aa_onehot_encoder):
    encoded = encoder.transform(list(sequence))
    onehot_encoded = onehot_encoder.transform(encoded.reshape(-1, 1))
    return onehot_encoded

def encode_structures(structures, encoder=structure_encoder):
    encoded = encoder.transform(list(structures))
    return encoded

def load_data(filepath):
    with open(filepath, 'rb') as file:
        data = pickle.load(file)
    sequences = data['sequences']
    structures = data['structures']
    return sequences, structures

def save_data_seclib(sequences, structures, output_file):
    with open(output_file, 'w') as f:
        for seq, struct in zip(sequences, structures):
            # Für jede Sequenz und Struktur, schreibe sie in die Datei
            f.write(f">{output_file}\n")  # Eindeutiger Bezeichner für die Sequenz
            f.write(f"{seq}\n")  # Die Aminosäuresequenz
            f.write(f"{struct}\n")  # Die Sekundärstruktur


def main():
    sequences, structures = load_data("path_to_your_preprocessed_data")

    # Codieren der Sequenzen und Strukturen
    encoded_sequences = np.array([encode_sequence(seq) for seq in sequences])
    encoded_structures = encode_structures(structures)

    # Aufteilung in Trainings- und Testsets
    X_train, X_test, y_train, y_test = train_test_split(encoded_sequences, encoded_structures, test_size=0.2, random_state=42)

    # Speichern der Sets
    save_data((X_train, y_train), "train_data.pkl")
    save_data((X_test, y_test), "test_data.pkl")
    print("Trainings- und Testdaten wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    main()
