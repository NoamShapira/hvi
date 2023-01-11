HOST_PROTEIN="$1"
VIRUS_PROTEIN="$2"
RESULTS_DIR="$3"

# configuration
#SCRIPTS_REPO_DIR=/home/labs/sorek/noamsh/human_virus_interactions/hvi
ALPHAFOLD_REPO_DIR=/home/labs/sorek/noamsh/alphafold

NUM_PREDICTION_PER_MODEL="1"

HOST_VIRUS="${HOST_PROTEIN}_${VIRUS_PROTEIN}"
COMBINED_FASTA_PATH="${RESULTS_DIR}/${HOST_VIRUS}/${HOST_VIRUS}.fasta"

module load Singularity; singularity exec --nv /apps/containers/singularity/AlphaFold-2.2.0-foss-2021a-CUDA-11.3.1.sif python "$ALPHAFOLD_REPO_DIR"/run_alphafold_msa_generation.py --fasta_paths="$COMBINED_FASTA_PATH" --output_dir="$RESULTS_DIR" --max_template_date=2022-01-01 --model_preset=multimer --data_dir=/shareDB/alphafold/ --uniref90_database_path=/shareDB/alphafold/uniref90/uniref90.fasta --mgnify_database_path=/shareDB/alphafold/mgnify/mgy_clusters_2018_12.fa --template_mmcif_dir=/shareDB/alphafold/pdb_mmcif/mmcif_files --obsolete_pdbs_path=/shareDB/alphafold/pdb_mmcif/obsolete.4.dat --bfd_database_path=/shareDB/alphafold/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt --uniclust30_database_path=/shareDB/alphafold/uniclust30/uniclust30_2018_08/uniclust30_2018_08 --pdb_seqres_database_path=/shareDB/alphafold/pdb_seqres/pdb_seqres.1.txt --uniprot_database_path=/shareDB/alphafold/uniprot/uniprot.fasta --use_gpu_relax=false --use_precomputed_msas=true --run_relax=false --num_multimer_predictions_per_model="$NUM_PREDICTION_PER_MODEL" --benchmark=false