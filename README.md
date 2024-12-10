
# MutScan

[![Nextflow](https://img.shields.io/badge/Nextflow->=22.10.1-brightgreen.svg?style=flat&logo=nextflow)](https://www.nextflow.io/)
[![Docker Profile](https://img.shields.io/badge/Profile-Docker-blue.svg?logo=docker)](#)
[![Singularity Profile](https://img.shields.io/badge/Profile-Singularity-blueviolet.svg?logo=singularity)](#)
[![Conda Profile](https://img.shields.io/badge/Profile-Conda-green.svg?logo=conda)](#)

**MutScan** is a **Nextflow** pipeline designed for scalable, reproducible, and streamlined mutation scanning in genomic data. It integrates **Nextclade** for variant analysis and a Python-based analysis workflow for identifying and summarizing curated mutations. The pipeline accommodates various runtime environments—including Docker, Singularity, and Conda—ensuring portability across diverse computational settings.

## Key Features

- **Integrated Workflow**: Seamlessly orchestrates data preparation, Nextclade analysis, TSV cleaning, mutation analysis, and final data compilation.
- **Curated Mutation Screening**: Matches detected variants against a user-provided curated mutation list, including combination mutations, facilitating targeted variant discovery.
- **Scalable & Portable**: Harnesses Nextflow’s parallelization for large datasets, and leverages containerization (Docker, Singularity, Conda) for reproducible environments.
- **Reproducibility & Transparency**: Detailed log files, trace data, and reports ensure results are transparent and easily reproducible.

## Use Cases

1. **Public Health Genomics**: Identify, track, and summarize clinically relevant mutations (e.g., in viral pathogens).
2. **Evolutionary Studies**: Monitor mutation emergence and patterns across multiple datasets or time points.
3. **Diagnostic Validation**: Rapidly integrate curated mutations to enhance diagnostic pipelines and ensure consistent QC checks.

## Pipeline Overview

The MutScan pipeline comprises several steps:

1. **Data Preparation**:  
   - Validates and organizes input FASTA files.
   - Ensures uniform file naming and structure.

2. **Nextclade Analysis**:  
   - Runs Nextclade on input FASTA files against specified datasets.
   - Generates per-dataset TSVs capturing identified mutations and related metadata.

3. **TSV Cleaning**:  
   - Filters raw TSV outputs, removing empty or irrelevant records.
   - Produces cleaned TSV files suitable for downstream analysis.

4. **Mutation Analysis**:  
   - Uses a curated mutations CSV to identify known and important mutations.
   - Distinguishes curated, inferred, and combination mutations.
   - Produces summaries and frequency tables for each dataset.

5. **Data Compilation**:  
   - Aggregates per-dataset results into unified summary CSVs.
   - Produces `Mutation_List.csv` and `Mutation_Counts.csv` consolidating all findings.

## Quick Start

### Requirements

- **Nextflow**: Version >=22.10.1  
- **Container or Environment**:
  - Docker  
  or
  - Singularity  
  or
  - Conda environment with required packages

- **Data Inputs**:
  - A directory with FASTA files.
  - A curated mutations CSV.
  - A directory of Nextclade datasets.

### Example Command

```bash
nextflow run main.nf \
    -profile docker \
    --input_dir "/path/to/input_fasta" \
    --output_dir "/path/to/results" \
    --mutations_csv "/path/to/mutations.csv" \
    --nextclade_datasets "/path/to/nextclade_datasets"
```

**Key Parameters:**
- `--input_dir`: Directory containing FASTA files.
- `--output_dir`: Directory for all pipeline outputs.
- `--mutations_csv`: Curated mutations CSV file.
- `--nextclade_datasets`: Directory with Nextclade datasets.

**Profiles:**
- `-profile docker` for Docker containers.
- `-profile singularity` for Singularity images.
- `-profile conda` for Conda environments.

### Optional Parameters

- `--max_memory`, `--max_time`, `--max_cpus` to set resource limits.
- Use `-profile slurm` for SLURM-based HPC systems.

## Output Structure

After pipeline completion, the `--output_dir` will contain:

- **`Mutation_Scan/`**: Processed FASTA files.
- **`nextclade_outputs/`**: Raw Nextclade TSV output.
- **`cleaned_tsv/`**: Cleaned TSV files for analysis.
- **`mutation_results/`**: Per-dataset mutation summaries and frequency tables.
- **`combined_results/`**: Final combined `Mutation_List.csv` and `Mutation_Counts.csv`.
- **`pipeline_info/`**: Execution logs, trace files, timeline, reports, and DAG visualization.

## Pipeline Workflow

[nf-mutscan workflow](images/nf-mutscan-workflow.png)

## Customization

- Update `mutations_csv` with new curated mutations.
- Modify `max_cpus`, `max_memory`, and `max_time` in `nextflow.config` to match resource availability.
- Extend or adapt profiles for other HPC or cloud environments.