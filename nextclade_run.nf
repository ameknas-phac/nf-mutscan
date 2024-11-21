process NEXTCLADE_RUN {
    tag 'Nextclade Analysis'

    conda 'bioconda::nextclade==3.9.1--h9ee0642_0'  // Adjust the version as needed
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container 'https://depot.galaxyproject.org/singularity/nextclade:3.9.1--h9ee0642_0'
    } else {
        container 'quay.io/biocontainers/nextclade:3.9.1--h9ee0642_0'
    }

    input:
    path fasta_files
    path ch_nextclade_datasets
    
    output:
    path ('nextclade_outputs'), emit: nextclade_outputs

    publishDir "${params.output_dir}", mode: 'copy'

    script:
    """
    mkdir -p nextclade_outputs

    for dataset in ${ch_nextclade_datasets}/*; do
        dataset_name=\$(basename \${dataset})
        echo "Running Nextclade on dataset: \${dataset_name}"
        nextclade run \
            ${fasta_files}/*.fasta \
            --output-tsv nextclade_outputs/\${dataset_name}.tsv \
            --input-dataset \${dataset}
    done
    """
}