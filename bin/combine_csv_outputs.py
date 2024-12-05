#!/usr/bin/env python3

import os
import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Combine and split processed mutation analysis CSV files.')
    parser.add_argument('-i', '--input_dir', required=True, help='Directory containing the mutation analysis CSV files.')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory to save the separated output CSV files.')
    return parser.parse_args()

def process_csv_files(input_dir):
    mutation_list_data = []
    count_data = []
    
    # Collect all the mutation summary CSV files (excluding freq_summary files)
    mutation_summary_files = [
        f for f in os.listdir(input_dir)
        if f.endswith('_summary.csv') and not f.endswith('_freq_summary.csv')
    ]
    
    # Collect all the frequency summary CSV files
    freq_summary_files = [f for f in os.listdir(input_dir) if f.endswith('_freq_summary.csv')]
    
    if not mutation_summary_files:
        raise FileNotFoundError(f"No mutation '_summary.csv' files found in {input_dir}")
    
    if not freq_summary_files:
        raise FileNotFoundError(f"No '_freq_summary.csv' files found in {input_dir}")
    
    # Process mutation summary files for Mutation_List.csv
    for csv_file in mutation_summary_files:
        # Correctly extract the mutation list name
        mutation_list_name = os.path.basename(csv_file).split('_summary.csv')[0]
        file_path = os.path.join(input_dir, csv_file)
        
        # Read the CSV file
        df = pd.read_csv(file_path, skip_blank_lines=True)
        
        # Add the 'Mutation_List' column
        df['Mutation_List'] = mutation_list_name
        
        # Define columns for mutation list
        mutation_list_columns = [
            'Sequence_ID', 'All_Mutations', 'Curated_Mutations', 'Inferred_Mutations',
            'Combination_Present', 'Mutation_List'
        ]
        
        # Select the relevant columns
        mutation_list_df = df[mutation_list_columns]
        mutation_list_data.append(mutation_list_df)
    
    # Process frequency summary files for Mutation_Counts.csv
    for csv_file in freq_summary_files:
        # Correctly extract the mutation list name
        mutation_list_name = os.path.basename(csv_file).split('_freq_summary.csv')[0]
        file_path = os.path.join(input_dir, csv_file)
        
        # Read the CSV file
        df = pd.read_csv(file_path, skip_blank_lines=True)
        
        # Add the 'Mutation_List' column
        df['Mutation_List'] = mutation_list_name
        
        # Define columns for counts
        count_columns = ['Mutation_List', 'Mutation/Combination', 'Count', 'Type', 'Frequency']
        
        # Select the relevant columns
        count_df = df[count_columns]
        count_data.append(count_df)
    
    # Concatenate all the dataframes into single ones
    mutation_list_combined_df = pd.concat(mutation_list_data, ignore_index=True)
    count_combined_df = pd.concat(count_data, ignore_index=True)
    
    return mutation_list_combined_df, count_combined_df

def save_separated_files(mutation_list_df, count_df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the separate CSV files
    mutation_list_file = os.path.join(output_dir, 'Mutation_List.csv')
    count_file = os.path.join(output_dir, 'Mutation_Counts.csv')
    
    mutation_list_df.to_csv(mutation_list_file, index=False)
    count_df.to_csv(count_file, index=False)
    
    print(f"Mutation List saved to: {mutation_list_file}")
    print(f"Mutation Counts saved to: {count_file}")

def main():
    args = parse_arguments()
    
    # Process CSV files to get mutation list and counts DataFrames
    mutation_list_df, count_df = process_csv_files(args.input_dir)
    
    # Save the separated files
    save_separated_files(mutation_list_df, count_df, args.output_dir)

if __name__ == '__main__':
    main()
