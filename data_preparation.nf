process DATA_PREPARATION {
    tag 'Data Preparation'

    conda 'python==3.9'
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container 'https://depot.galaxyproject.org/singularity/python:3.9'
    } else {
        container 'quay.io/biocontainers/python:3.9'
    }

    input:
    path input_dir

    output:
    path ('Mutation_Scan'), emit: fasta_files

    publishDir "${params.output_dir}", mode: 'copy'

    script:
    """
    mkdir -p Mutation_Scan
    data_preparation.py -i ${input_dir} -o Mutation_Scan
    """
}