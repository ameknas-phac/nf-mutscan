process DATA_COMPILATION {
    tag 'Data Compilation'

    conda 'bioconda::mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6==fccb0c41a243c639e11dd1be7b74f563e624fcca-0'  // Adjust the version as needed
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container 'https://depot.galaxyproject.org/singularity/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    } else {
        container 'quay.io/biocontainers/mulled-v2-2076f4a3fb468a04063c9e6b7747a630abb457f6:fccb0c41a243c639e11dd1be7b74f563e624fcca-0'
    }


    input:
    path mutation_results

    output:
    path ('combined_results'), emit: combined_results_dir 
    
    publishDir "${params.output_dir}", mode: 'copy'

    script:
    """
    mkdir -p combined_results

    combine_csv_outputs.py -i ${mutation_results} -o combined_results
    """
}