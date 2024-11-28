#!/usr/bin/env python3

import argparse
import pandas as pd
from collections import Counter

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract mutations from a single TSV file and compare against curated mutations.')
    parser.add_argument('-i', '--input_file', required=True, help='TSV file containing results from multiple samples.')
    parser.add_argument('-o', '--output_prefix', default='mutation_summary', help='Prefix for the output CSV file(s).')
    parser.add_argument('-m', '--mutations_csv', required=False, help='Path to CSV file containing curated mutations in the format: Gene, AminoAcid, Combination, Reason_for_Inclusion.')
    return parser.parse_args()

# Function to load curated mutations from a CSV file
def load_curated_mutations(mutations_csv):
    mutations_df = pd.read_csv(mutations_csv, keep_default_na=False)
    if not {'Gene', 'AminoAcid', 'Combination', 'Reason_for_Inclusion'}.issubset(mutations_df.columns):
        raise ValueError("The mutations CSV must contain 'Gene', 'AminoAcid', 'Combination', and 'Reason_for_Inclusion' columns.")

    individual_mutations = []
    combination_mutations = {}
    
    for _, row in mutations_df.iterrows():
        if '+' in row['AminoAcid']:  # Combination
            combination = [f"{row['Gene']}:{mut}" for mut in row['AminoAcid'].split('+')]
            combination_mutations[row['AminoAcid']] = combination
        else:
            mutation_key = f"{row['Gene']}:{row['AminoAcid']}"
            individual_mutations.append(mutation_key)
    
    return individual_mutations, combination_mutations

# Function to match mutations, handle wildcard "X", and manage unexpected formats
def match_mutation(mutation, curated_list):
    try:
        if '-' in mutation or ':' not in mutation:
            return False

        gene, aa = mutation.split(":", 1)  # Split into gene and amino acid
    except ValueError:
        print(f"Warning: Unable to process mutation '{mutation}'")
        return False
    
    for curated in curated_list:
        curated_gene, curated_aa = curated.split(":", 1)
        if gene == curated_gene:
            if 'X' in curated_aa and aa[:-1] == curated_aa[:-1]:
                return True
            elif aa == curated_aa:
                return True
    return False

# Function to extract codon positions from mutations
def extract_codon_position(mutation):
    return ''.join(filter(str.isdigit, mutation.split(":")[1]))

# Function to infer mutations based on absence in the All_Mutations list
def infer_mutations(all_mutations, individual_mutations):
    inferred = []
    all_positions = {extract_codon_position(mut) for mut in all_mutations}
    for curated_mut in individual_mutations:
        curated_pos = extract_codon_position(curated_mut)
        # If the position is not in the list of all mutations, infer that the reference amino acid is present
        if curated_pos not in all_positions:
            gene, aa_curated = curated_mut.split(':')
            ref_aa = aa_curated[0]  # Take the reference amino acid
            inferred.append(f"{gene}:{ref_aa}{curated_pos}{ref_aa}")  # Format as HA:E75E for no change
    return inferred

# Function to check mutation combinations across both curated and inferred mutations
def check_combination_mutations(curated_mutations, inferred_mutations, combination_mutations):
    all_mutations = set(curated_mutations.split(', ') + inferred_mutations.split(', '))
    found_combinations = []
    
    for combination_key, mutation_combination in combination_mutations.items():
        if all(mut in all_mutations for mut in mutation_combination):
            found_combinations.append(combination_key)
    
    return found_combinations

# Function to process a TSV file
def process_file(input_file, output_prefix, individual_mutations, combination_mutations):
    df = pd.read_csv(input_file, sep='\t')

    if 'aaSubstitutions' not in df.columns or 'seqName' not in df.columns:
        raise ValueError("The input TSV must contain 'aaSubstitutions' and 'seqName' columns.")
    
    df['all_mutations'] = df[['aaSubstitutions', 'aaDeletions', 'aaInsertions']].fillna('').apply(
        lambda row: ','.join([x for x in row if x]), axis=1
    )

    # Output all mutations for each sample
    df['All_Mutations'] = df['all_mutations']

    # Check for curated mutations
    df['Curated_Mutations'] = df['all_mutations'].apply(
        lambda x: ', '.join([mut for mut in x.split(',') if match_mutation(mut, individual_mutations)]) if pd.notna(x) else "None"
    )

    # Infer mutations based on absence in the All_Mutations list
    df['Inferred_Mutations'] = df.apply(
        lambda row: ', '.join(infer_mutations(row['All_Mutations'].split(','), individual_mutations))
        if pd.notna(row['all_mutations']) else "None", axis=1
    )

    # Remove duplicates in Inferred_Mutations before cross-referencing
    df['Inferred_Mutations'] = df['Inferred_Mutations'].apply(
        lambda x: ', '.join(dict.fromkeys(x.split(', ')))
    )

    # Check for combinations across both curated and inferred mutations
    df['Combination_Present'] = df.apply(
        lambda row: ', '.join(check_combination_mutations(row['Curated_Mutations'], row['Inferred_Mutations'], combination_mutations))
        if pd.notna(row['Curated_Mutations']) and pd.notna(row['Inferred_Mutations']) else "None", axis=1
    )

    # Save the tables
    df[['seqName', 'All_Mutations', 'Curated_Mutations', 'Inferred_Mutations', 'Combination_Present']].rename(
        columns={'seqName': 'Sequence_ID'}
    ).to_csv(f"{output_prefix}_summary.csv", index=False)

    # Generate count and frequency tables
    create_frequency_table(df, individual_mutations, combination_mutations, output_prefix)

def create_frequency_table(df, individual_mutations, combination_mutations, output_prefix):
    mutation_counter = Counter()
    combination_counter = Counter()
    inferred_counter = Counter()

    for _, row in df.iterrows():
        all_mutations = row['All_Mutations'].split(',')
        for mut in all_mutations:
            mut = mut.strip()
            if mut and mut != "None":
                mutation_counter[mut] += 1

        if pd.notna(row['Combination_Present']) and row['Combination_Present'] != "None":
            for comb in row['Combination_Present'].split(', '):
                if comb:
                    combination_counter[comb] += 1

        inferred_mutations = row['Inferred_Mutations'].split(',')
        for inferred in inferred_mutations:
            inferred = inferred.strip()
            if inferred and inferred != "None":
                inferred_counter[inferred] += 1

    # Prepare mutation frequency DataFrame
    mutation_df = pd.DataFrame(list(mutation_counter.items()), columns=['Mutation/Combination', 'Count'])
    mutation_df['Type'] = 'Individual'

    combination_df = pd.DataFrame(list(combination_counter.items()), columns=['Mutation/Combination', 'Count'])
    combination_df['Type'] = 'Combination'

    inferred_df = pd.DataFrame(list(inferred_counter.items()), columns=['Mutation/Combination', 'Count'])
    inferred_df['Type'] = 'Inferred'

    # Merge all frequency DataFrames and calculate frequency
    combined_df = pd.concat([mutation_df, combination_df, inferred_df])
    combined_df['Frequency'] = combined_df['Count'] / df.shape[0]

    combined_df.to_csv(f"{output_prefix}_freq_summary.csv", index=False)

if __name__ == '__main__':
    args = parse_arguments()
    individual_mutations, combination_mutations = load_curated_mutations(args.mutations_csv) if args.mutations_csv else ([], {})
    process_file(args.input_file, args.output_prefix, individual_mutations, combination_mutations)