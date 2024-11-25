#!/usr/bin/env python3

import sys
import os
import pandas as pd

def clean_tsv_file(input_file, output_file):
    # Read the TSV file using pandas
    df = pd.read_csv(input_file, sep='\t', dtype=str)

    # Check if the DataFrame is empty
    if df.empty:
        print(f"Warning: {input_file} is empty.")
        return

    # Filter rows where the 4th column is not empty
    # pandas uses zero-based indexing, so column index 3 is the 4th column
    df = df[df.iloc[:, 3].notna() & (df.iloc[:, 3] != '')]

    # Remove any completely empty rows (if any)
    df.dropna(how='all', inplace=True)

    # Write the cleaned DataFrame back to a TSV file
    df.to_csv(output_file, sep='\t', index=False)

    print(f"Cleaned {input_file}, saved to {output_file}")

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith('.tsv'):
            input_file = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_cleaned.tsv"
            output_file = os.path.join(output_dir, output_filename)
            clean_tsv_file(input_file, output_file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: clean_tsv.py <input_dir> <output_dir>")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main(input_dir, output_dir)
