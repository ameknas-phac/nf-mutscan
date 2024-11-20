#!/usr/bin/env nextflow
process TestConfig {
    tag 'Test Config'

    script:
    """
    echo "Testing configuration settings..."
    echo "Input File: ${params.input_dir}"
    echo "Output Prefix: ${params.output_dir}"
    echo "Mutations CSV: ${params.mutations_csv}"
    echo "Profile : ${workflow.profile}"
    echo "Max Memory: ${params.max_memory}"
    echo "Max Time: ${params.max_time}"
    echo "Max CPUs: ${params.max_cpus}"
    """
}

workflow {
    TestConfig()
}