#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { DATA_PREPARATION } from './data_preparation.nf'

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

    // Sample Sheet Check
    ch_input = DATA_PREPARATION(Channel.fromPath(params.input_dir, checkIfExists: true))

    //DATA_PREPARATION(params.input_dir)

    // Test configuration
    TestConfig()
}