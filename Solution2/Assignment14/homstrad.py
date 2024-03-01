import os
import re


def main():
    root_dir = '/home/anna/Documents/Blockteil/2019_Feb'

    for subdir, dirs, files in os.walk(root_dir):
        # Sort directories and files to ensure a predictable order
        dirs.sort()
        files.sort()

        ali_files = [file for file in files if file.endswith('.ali')]
        tem_files = [file for file in files if file.endswith('.tem')]

        # Process .ali files first, then .tem files
        for file in ali_files + tem_files:
            file_path = os.path.join(subdir, file)
            if file.endswith('.ali'):
                family_name = parse_ali_file(file_path)
                print(f"Processing .ali file: {file}")
                print(f"Family Name: {family_name}\n")
            elif file.endswith('.tem'):
                print(f"Processing .tem file: {file}")
                pdb_data = parse_tem_file(file_path)
                for pdb_id, details in pdb_data.items():
                    print(
                        f"PDB ID: {pdb_id}, Chain: {details['chain']}, Sequence: {details['sequence'][:25]}..., Secondary Structure: {details['secondary_structure'][:25]}...\n")


def parse_ali_file(file_path):
    family_pattern = re.compile(r'^C; family: (.*)')
    family_name = None

    with open(file_path, 'r') as file:
        for line in file:
            match = family_pattern.match(line)
            if match:
                family_name = match.group(1).strip()
                break
    return family_name


def parse_tem_file(file_path):
    # Patterns
    pdb_id_pattern = re.compile(r'^>P1;(\w{4})(\w?)')
    sequence_pattern = re.compile(r'^sequence$')
    sec_str_pattern = re.compile(r'^secondary structure and phi angle$')
    stop_pattern = re.compile(r'^solvent accessibility$')

    pdb_id_to_content_type = {}
    current_pdb_id = None
    current_content_type = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Once 'solvent accessibility' is found, stop processing further for the current file
            if stop_pattern.match(line):
                break

            pdb_id_match = pdb_id_pattern.match(line)
            if pdb_id_match:
                current_pdb_id = pdb_id_match.group(1)
                chain = pdb_id_match.group(2) if pdb_id_match.group(2) else None  # Chain is None if not present
                # Initialize pdb_id_to_content_type structure for the PDB ID
                if current_pdb_id not in pdb_id_to_content_type:
                    pdb_id_to_content_type[current_pdb_id] = {'chain': chain, 'sequence': '', 'secondary_structure': ''}
                current_content_type = None  # Reset current_content_type whenever a new PDB ID is encountered
                continue

            if sequence_pattern.match(line) or sec_str_pattern.match(line):
                current_content_type = 'sequence' if sequence_pattern.match(line) else 'secondary_structure'
                continue

            if current_pdb_id and current_content_type:
                # Append line to the correct part of current PDB ID's data
                pdb_id_to_content_type[current_pdb_id][current_content_type] += line

    return pdb_id_to_content_type


if __name__ == "__main__":
    main()
