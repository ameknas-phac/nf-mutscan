#!/usr/bin/env python3

import os
import sys
import pandas as pd


def validate_mutation_files(mutation_dir):
    """
    Validate mutation files in the given directory.

    Parameters:
    - mutation_dir (str): Path to the directory containing mutation CSV files.

    Raises:
    - FileNotFoundError: If no valid mutation files are found.
    - ValueError: If a file is invalid.
    """

    if not os.path.exists(mutation_dir):
        raise FileNotFoundError(f"ERROR: Mutation directory '{mutation_dir}' does not exist.")

    csv_files = [f for f in os.listdir(mutation_dir) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"ERROR: No CSV files found in mutation directory '{mutation_dir}'.")

    for file in csv_files:
        file_path = os.path.join(mutation_dir, file)
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"ERROR: Failed to read file '{file_path}'. Reason: {e}")

        # Validate header
        expected_columns = {'Gene', 'AminoAcid', 'Combination', 'Reason_for_Inclusion'}
        if not expected_columns.issubset(df.columns):
            raise ValueError(
                f"ERROR: File '{file_path}' is missing required columns. "
                f"Expected columns: {expected_columns}, Found: {set(df.columns)}"
            )

        # Check for non-header rows
        if df.shape[0] == 0:
            raise ValueError(f"ERROR: File '{file_path}' contains only a header and no data.")
        print(f"File '{file}' passed validation.")  # Optional for debugging purposes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_mutation_files.py <mutation_dir>")
        sys.exit(1)

    mutation_dir = sys.argv[1]

    try:
        validate_mutation_files(mutation_dir)
        print(f"All files in '{mutation_dir}' are valid.")
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
