#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { DATA_PREPARATION } from './data_preparation.nf'
include { NEXTCLADE_RUN } from './nextclade_run.nf'
include { CLEAN_TSV_FILES } from './clean_tsv_files.nf'

process TestConfig {
    tag 'Test Config'

    script:
    """
    echo "Testing configuration settings..."
    echo "Input Directory: ${params.input_dir}"
    echo "Output Directory: ${params.output_dir}"
    echo "Mutations CSV: ${params.mutations_csv}"
    echo "Profile: ${workflow.profile}"
    echo "NEXTCLADE DATA: ${params.nextclade_datasets}"
    echo "Max Memory: ${params.max_memory}"
    echo "Max Time: ${params.max_time}"
    echo "Max CPUs: ${params.max_cpus}"
    """
}

workflow {
    // Convert parameters to channels
    ch_versions = Channel.empty()

    // Data Prep
    ch_input = DATA_PREPARATION(Channel.fromPath(params.input_dir, checkIfExists: true))

    // Run Nextclade
    NEXTCLADE_RUN(DATA_PREPARATION.out.fasta_files, Channel.fromPath(params.nextclade_datasets))

    // Clean TSV Files from Nextclade
    CLEAN_TSV_FILES(NEXTCLADE_RUN.out.nextclade_outputs)

    // Test configuration
    TestConfig()
}