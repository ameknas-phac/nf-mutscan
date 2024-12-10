process MUTATION_ANALYSIS {
    tag 'Mutation Analysis'

    conda 'bioconda::mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6==fccb0c41a243c639e11dd1be7b74f563e624fcca-0'  // Adjust the version as needed
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container 'https://depot.galaxyproject.org/singularity/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    } else {
        container 'quay.io/biocontainers/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    }


    input:
    path cleaned_tsv_files
    path mutations_dir

    output:
    path 'mutation_results', emit: mutation_results

    publishDir "${params.output_dir}", mode: 'copy'

    script:
    """
    mkdir -p mutation_results

    validate_mutation_files.py ${mutations_dir} || exit 1

    run_mutation_analysis.py \\
        -t ${cleaned_tsv_files} \\
        -m ${mutations_dir} \\
        -d ${params.nextclade_datasets}\\
        -s ${params.mutation_script} \\
        -o mutation_results
    """
}