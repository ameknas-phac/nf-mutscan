#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run mutation analysis on cleaned TSV files with corresponding mutation lists.')
    parser.add_argument('-t', '--tsv_dir', required=True, help='Directory containing cleaned TSV files.')
    parser.add_argument('-m', '--mutations_dir', required=True, help='Directory containing mutation list CSV files.')
    parser.add_argument('-d', '--nextclade_datasets', required=True, help='Directory containing Nextclade datasets.')
    parser.add_argument('-s', '--mutation_script', required=True, help='Path to the mutation analysis script (mutation_screen_vNextGen.py).')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory to store mutation analysis results.')
    return parser.parse_args()

def find_matching_file(base_name, files, file_type):
    """
    Finds a file in the provided list where the base_name appears as a substring.
    Raises an error if no match is found or if multiple matches are found.
    """
    matches = [f for f in files if base_name in f]
    if len(matches) == 0:
        print(f"Error: No matching {file_type} file found for dataset '{base_name}'", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: Multiple matching {file_type} files found for dataset '{base_name}': {matches}", file=sys.stderr)
        sys.exit(1)
    return matches[0]

def main():
    args = parse_arguments()

    tsv_dir = args.tsv_dir
    mutations_dir = args.mutations_dir
    nextclade_datasets_dir = args.nextclade_datasets
    mutation_script = args.mutation_script
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)

    # Collect dataset names from nextclade datasets directory
    dataset_names = [name for name in os.listdir(nextclade_datasets_dir) if os.path.isdir(os.path.join(nextclade_datasets_dir, name))]

    # Collect cleaned TSV and mutation list files
    tsv_files = os.listdir(tsv_dir)
    mutation_files = os.listdir(mutations_dir)

    # Match datasets, TSV files, and mutation files
    for dataset_name in dataset_names:
        matching_tsv_file = find_matching_file(dataset_name, tsv_files, "TSV")
        matching_mutation_file = find_matching_file(dataset_name, mutation_files, "mutation list")

        matching_tsv_path = os.path.join(tsv_dir, matching_tsv_file)
        matching_mutation_path = os.path.join(mutations_dir, matching_mutation_file)
        output_prefix = os.path.join(output_dir, dataset_name)

        print(f"Processing {matching_tsv_path} with {matching_mutation_path}")

        cmd = [
            'python', mutation_script,
            '-i', matching_tsv_path,
            '-m', matching_mutation_path,
            '-o', output_prefix
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully processed {matching_tsv_path} with {matching_mutation_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {matching_tsv_path} with {matching_mutation_path}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()