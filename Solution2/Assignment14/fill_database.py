import os
import re
import mysql.connector
from mysql.connector import Error

# Constants for the database connection
DB_HOST = 'mysql2-ext.bio.ifi.lmu.de'
DB_USER = 'bioprakt13'
DB_PASSWORD = '$1$S4kE4pw1$8ANT55zOf1nKHgoau9K0A0'
DB_NAME = 'bioprakt13'
ROOT_DIR = '/mnt/biocluster/praktikum/bioprakt/Data/HOMSTRAD_DB/2019_Feb'



# Regex patterns for parsing files
PDB_ID_PATTERN = re.compile(r'^>P1;(\w{4})(\w*)')
SEQUENCE_PATTERN = re.compile(r'^sequence$')
SEC_STR_PATTERN = re.compile(r'^secondary structure and phi angle$')
STOP_PATTERN = re.compile(r'^solvent accessibility$')

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def insert_family_name(cursor, family_name):
    """Inserts a family name into the Homestrad table and returns the generated a_id."""
    query = "INSERT INTO Homestrad (family_name) VALUES (%s)"
    cursor.execute(query, (family_name,))
    return cursor.lastrowid

def insert_alignments(cursor, a_id, pdb_id, chain, aligned_sequence, aligned_sec_structure):
    """Inserts an alignment record into the Alignments table."""
    query = (
        "INSERT INTO Alignments (a_id, pdb_id, chain, aligned_sequence, aligned_sec_structure) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    cursor.execute(query, (a_id, pdb_id, chain, aligned_sequence, aligned_sec_structure))

def insert_is_fam(cursor, a_id, fam_id):
    """Inserts a record into the is_fam table to link alignments and families."""
    query = "INSERT INTO is_fam (a_id, fam_id) VALUES (%s, %s)"
    cursor.execute(query, (a_id, fam_id))


def parse_tem_file(file_path):
    """Parses .tem files to extract PDB IDs and associated data."""
    pdb_id_to_content_type = {}
    current_pdb_id, current_chain, current_content_type = None, None, None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if STOP_PATTERN.match(line):
                break

            pdb_id_match = PDB_ID_PATTERN.match(line)
            if pdb_id_match:
                current_pdb_id = pdb_id_match.group(1)
                current_chain = pdb_id_match.group(2) or ' '
                # Create a composite key using both pdbId and chain
                composite_key = (current_pdb_id, current_chain)
                if composite_key not in pdb_id_to_content_type:
                    pdb_id_to_content_type[composite_key] = {'sequence': '', 'secondary_structure': ''}
                continue

            sequence_match = SEQUENCE_PATTERN.match(line)
            if sequence_match:
                current_content_type = 'sequence'
                continue

            sec_str_match = SEC_STR_PATTERN.match(line)
            if sec_str_match:
                current_content_type = 'secondary_structure'
                continue

            if composite_key and current_content_type:
                pdb_id_to_content_type[composite_key][current_content_type] += line

    return pdb_id_to_content_type


def main():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        for family_name in os.listdir(ROOT_DIR):
            family_path = os.path.join(ROOT_DIR, family_name)
            if os.path.isdir(family_path):
                a_id = insert_family_name(cursor, family_name)
                print(f"Inserted family name: {family_name} with ID {a_id}")
                for file_name in os.listdir(family_path):
                    file_path = os.path.join(family_path, file_name)
                    if file_name.endswith('.tem'):
                        pdb_data = parse_tem_file(file_path)
                        for (pdb_id, chain), content in pdb_data.items():
                            insert_alignments(cursor, a_id, pdb_id, chain, content['sequence'], content['secondary_structure'])
                            insert_is_fam(cursor, a_id, a_id)
                            print(f"Inserted data for PDB ID: {pdb_id}, Chain: {chain}")
                        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")




if __name__ == "__main__":
    main()