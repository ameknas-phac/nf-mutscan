process CLEAN_TSV_FILES {

    tag 'Clean TSV Files'

    conda 'bioconda::mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6==fccb0c41a243c639e11dd1be7b74f563e624fcca-0'  // Adjust the version as needed
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container 'https://depot.galaxyproject.org/singularity/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    } else {
        container 'quay.io/biocontainers/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    }


    input:
    path nextclade_outputs

    output:
    path ('cleaned_tsv'), emit: cleaned_tsv_files

    publishDir "${params.output_dir}", mode: 'copy'

    script:
    """
    mkdir -p cleaned_tsv

    clean_tsv.py ${nextclade_outputs} cleaned_tsv
    """
}