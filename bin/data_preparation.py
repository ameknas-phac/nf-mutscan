#!/usr/bin/env python3

import argparse
import os
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prepare FASTA files for processing.')
    parser.add_argument('-i', '--input_dir', required=True, help='Input directory containing FASTA files.')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory for processed files.')
    return parser.parse_args()

def copy_fasta_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(('.fasta', '.fa', '.consensus.fasta', '.irma.fasta', '.irma.consensus.fasta')):
            src = os.path.join(input_dir, file)
            dst = os.path.join(output_dir, file)
            shutil.copy(src, dst)

def rename_files_to_fasta(directory):
    valid_extensions = ['consensus.fasta', 'irma.fasta', 'fa', 'fasta', 'irma.consensus.fasta']
    new_extension = 'fasta'
    for file in os.listdir(directory):
        for ext in valid_extensions:
            if file.endswith(f".{ext}"):
                base = file.rsplit(f".{ext}", 1)[0]
                new_filename = f"{base}.{new_extension}"
                os.rename(os.path.join(directory, file), os.path.join(directory, new_filename))
                break  # Move to the next file after renaming

def main():
    args = parse_arguments()
    input_dir = args.input_dir
    output_dir = args.output_dir

    print(f"Copying FASTA files from {input_dir} to {output_dir}")
    copy_fasta_files(input_dir, output_dir)

    print(f"Renaming files in {output_dir} to have consistent .fasta extensions")
    rename_files_to_fasta(output_dir)

    print("Data preparation completed successfully.")

if __name__ == '__main__':
    main()