HOST_PROTEIN="$1"
VIRUS_PROTEIN="$2"

# configuration
SCRIPTS_REPO_DIR=/home/labs/sorek/noamsh/human_virus_interactions/hvi
ALPHAFOLD_REPO_DIR=/home/labs/sorek/noamsh/alphafold

NUM_PREDICTION_PER_MODEL="1"
DATASET="hvidb" # ban be hvidb or img_vr

# python environment for data organizing
module load miniconda/201904/python/3.7
conda activate noam_alphafold

if [ $DATASET == "img_vr" ]; then
  RESULTS_DIR=/home/labs/sorek/noamsh/AF_multimer_exercise/results/
  python "$SCRIPTS_REPO_DIR"/weizmann_scripts/prepare_result_dir_for_alphafold_on_img_vr.py --results_dir="$RESULTS_DIR" --bacteria_protein_name="$HOST_PROTEIN" --phage_protein_name="$VIRUS_PROTEIN"
fi

if [ $DATASET == "hvidb" ]; then
  RESULTS_DIR=/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold/
  python "$SCRIPTS_REPO_DIR"/weizmann_scripts/prepare_result_dir_for_alphafold_on_hvidb.py --results_dir="$RESULTS_DIR" --host_protein_name="$HOST_PROTEIN" --virus_protein_name="$VIRUS_PROTEIN"
fi

HOST_VIRUS="${HOST_PROTEIN}_${VIRUS_PROTEIN}"
COMBINED_FASTA_PATH="${RESULTS_DIR}/${HOST_VIRUS}/${HOST_VIRUS}.fasta"
# /apps/containers/singularity/AlphaFold-2.1.2-fosscuda-2020b-BETA.sif
# --env XLA_FLAGS="--xla_gpu_force_compilation_parallelism=1"
# --xla_force_host_platform_device_count=5
module load Singularity; singularity exec --nv /apps/containers/singularity/AlphaFold-2.2.0-foss-2021a-CUDA-11.3.1.sif python "$ALPHAFOLD_REPO_DIR"/run_alphafold.py --fasta_paths="$COMBINED_FASTA_PATH" --output_dir="$RESULTS_DIR" --max_template_date=2022-01-01 --model_preset=multimer --data_dir=/shareDB/alphafold/ --uniref90_database_path=/shareDB/alphafold/uniref90/uniref90.fasta --mgnify_database_path=/shareDB/alphafold/mgnify/mgy_clusters_2018_12.fa --template_mmcif_dir=/shareDB/alphafold/pdb_mmcif/mmcif_files --obsolete_pdbs_path=/shareDB/alphafold/pdb_mmcif/obsolete.4.dat --bfd_database_path=/shareDB/alphafold/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt --uniclust30_database_path=/shareDB/alphafold/uniclust30/uniclust30_2018_08/uniclust30_2018_08 --pdb_seqres_database_path=/shareDB/alphafold/pdb_seqres/pdb_seqres.1.txt --uniprot_database_path=/shareDB/alphafold/uniprot/uniprot.fasta --use_gpu_relax=true --use_precomputed_msas=true --run_relax=false --num_multimer_predictions_per_model="$NUM_PREDICTION_PER_MODEL" --benchmark=true

