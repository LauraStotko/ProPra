#!/usr/bin/env python

import argparse
import os


import pysam

def read_sam_file(samfile_path):
    """
    Reads a SAM file and returns an iterator over the aligned segments.
    Ensure the file exists before attempting to open it.
    """
    try:
        samfile = pysam.AlignmentFile(samfile_path, "r")
        return samfile.fetch()
    except FileNotFoundError:
        print(f"Error: SAM file '{samfile_path}' does not exist.")
        exit(1)
    except Exception as e:
        print(f"Error reading SAM file: {e}")
        exit(1)


def filter_no_off_targets(alignments):
    """
    Filters sequences that do not appear in the human genome with up to 3 mismatches.
    """
    no_off_targets = []
    for read in alignments:
        if read.get_tag("NM") <= 3 and not read.is_unmapped:
            no_off_targets.append(read)
    return no_off_targets


def filter_with_mismatch(alignments):
    """
    Filters sequences that appear in the human genome with up to 3 mismatches and errors in the GG suffix.
    """
    with_mismatch = []
    for read in alignments:
        if read.get_tag("NM") <= 3 and not read.is_unmapped:
            if check_gg_suffix_mismatch(read):
                with_mismatch.append(read)
    return with_mismatch


def check_gg_suffix_mismatch(read):
    """
    Checks if the mismatches in the alignment occur in the GG suffix.
    """
    md_tag = read.get_tag("MD")
    return "GG" in md_tag[-2:]  # Simplified assumption for demonstration purposes


def write_to_fasta(sequences, output_file):
    """
    Writes sequences to a FASTA file. Ensures that the directory for the output file exists.
    """
    try:
        with open(output_file, "w") as f:
            for seq in sequences:
                f.write(f">{seq.query_name}\n{seq.seq}\n")
    except Exception as e:
        print(f"Error writing to FASTA file '{output_file}': {e}")
        exit(1)


def parse_arguments():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description='Filter CRISPR off-targets and mismatches in SAM format.')
    parser.add_argument('--sam', type=str, required=True, help='Input SAM file path')
    parser.add_argument('--no-off-targets', type=str, required=True, help='Output file for no off-target sequences')
    parser.add_argument('--with-mismatch', type=str, required=True,
                        help='Output file for sequences with mismatches in GG suffix')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Check if the input SAM file exists before proceeding
    if not os.path.exists(args.sam):
        print(f"Error: The specified SAM file '{args.sam}' does not exist.")
        exit(1)

    # Read alignments from SAM file
    alignments = read_sam_file(args.sam)

    # Filter alignments
    no_off_targets = filter_no_off_targets(alignments)
    with_mismatch = filter_with_mismatch(alignments)

    # Write filtered sequences to FASTA files
    write_to_fasta(no_off_targets, args.no_off_targets)
    write_to_fasta(with_mismatch, args.with_mismatch)

main()

