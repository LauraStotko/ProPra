import argparse
import re

def read_csv(input_file):
    """Reads the CSV file and returns the col_names and rows."""
    col_names = input_file.readline().strip().split(',')
    rows = [line.strip().split(',') for line in input_file]
    return col_names, rows

def process_data(col_names, rows, experimental_factor):
    """Processes rows of data to gather required statistics."""
    data_type_counts = {}
    unique_antibodies_per_ctype = {}
    chosen_antibody_per_ctype = {}
    ctype_to_dcc_rna = {}
    ctype_to_dcc_chip = {}
    rna_seq_ctypes = set()

    # Map column names to indices for easier access
    col_indices = {name: index for index, name in enumerate(col_names)}

    # Adjustment for issues in encode.csv
    col_indices['DCC_Accession'] = -2

    for row in rows:
        data_type = row[col_indices['Data_Type']]
        ctype = row[col_indices['Cell_Type']]
        exp_factor = row[col_indices['Experimental_Factors']]
        dcc_accession = row[col_indices['DCC_Accession']]

        # Include 0 values for unique_antibodies
        if ctype not in unique_antibodies_per_ctype:
            unique_antibodies_per_ctype[ctype] = set()

        # Count occurrences for each data type for 9.1
        data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1

        if data_type == "ChIP-seq":
            process_chip_seq(ctype, exp_factor, dcc_accession, experimental_factor, unique_antibodies_per_ctype,
                             chosen_antibody_per_ctype, ctype_to_dcc_chip)

        elif data_type == "RNA-seq":
            rna_seq_ctypes.add(ctype)
            if dcc_accession != "":
                ctype_to_dcc_rna.setdefault(ctype, []).append(dcc_accession)

    antibodies_chip_counts = {ctype: len(antibodies) for ctype, antibodies in unique_antibodies_per_ctype.items()}
    combined_accessions = compile_combined_accessions(chosen_antibody_per_ctype, rna_seq_ctypes, ctype_to_dcc_rna,
                                                      ctype_to_dcc_chip)

    return data_type_counts, antibodies_chip_counts, combined_accessions


def process_chip_seq(ctype, exp_factor, dcc_accession, experimental_factor, unique_antibodies, chosen_antibodies,
                     ctype_to_dcc):
    """Processes ChIP-seq data for 9.2."""
    if exp_factor.startswith("Antibody"):
        antibody = exp_factor.split(" ", 1)[0]
        unique_antibodies.setdefault(ctype, set()).add(antibody)

    if re.match(f"^{re.escape(experimental_factor)}( |$)", exp_factor):
        chosen_antibodies.setdefault(ctype, []).append(exp_factor)
        if dcc_accession != "":
            ctype_to_dcc.setdefault(ctype, []).append(dcc_accession)


def compile_combined_accessions(chosen_antibodies, rna_seq_ctypes, rna_accessions, chip_accessions):
    """Compiles combined accessions for ChIP-seq and RNA-seq for 9.3."""
    combined = {ctype: {'RNA-seq': sorted(rna_accessions.get(ctype, [])),
                        'ChIP-seq': sorted(chip_accessions.get(ctype, []))}
                for ctype in chosen_antibodies if ctype in rna_seq_ctypes}
    return combined


def write_to_tsv_file(data, filepath):
    with open(filepath, 'w') as file:
        for key, value in sorted(data.items()):
            file.write(f"{key}\t{value}\n")


def write_combined_table(combined_accessions, filepath):
    with open(filepath, 'w') as file:
        file.write("cell line\tRNAseq Accession\tChIPseq Accession\n")
        for ctype, accessions in combined_accessions.items():
            rna_accessions_str = ",".join(accessions['RNA-seq'])
            chip_accessions_str = ",".join(accessions['ChIP-seq'])
            file.write(f"{ctype}\t{rna_accessions_str}\t{chip_accessions_str}\n")


def main():
    parser = argparse.ArgumentParser(description="Analyses CSV file and outputs specific TSV files")
    parser.add_argument("--input", type=argparse.FileType("r"), required=True, help="Path to the CSV file to be examined")
    parser.add_argument("--output", required=True, help="Destination file path for the analysis result in TSV format")
    parser.add_argument("--experimental-factor", default="Antibody=H3K27me3", help="Experimental factor to filter on")
    args = parser.parse_args()

    #with open(args.input, 'r') as input_file:
    col_names, rows = read_csv(args.input)
    data_type_counts, antibodies_chip_counts, combined_accessions = process_data(col_names, rows,
                                                                                 args.experimental_factor)

    # Write results to files
    write_to_tsv_file(data_type_counts, f"{args.output}/exptypes.tsv")
    write_to_tsv_file(antibodies_chip_counts, f"{args.output}/antibodies.tsv")
    write_combined_table(combined_accessions, f"{args.output}/chip_rna_seq.tsv")


if __name__ == "__main__":
    main()
