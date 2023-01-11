HOST_PROTEIN="$1"
VIRUS_PROTEIN="$2"
RESULTS_DIR="$3"

JOB_LOGS_DIR=/home/labs/sorek/noamsh/wexac_job_logs/"${HOST_PROTEIN}_${VIRUS_PROTEIN}"
mkdir -p "$JOB_LOGS_DIR"

MSA_GENERATION_SCRIPT=/home/labs/sorek/noamsh/human_virus_interactions/hvi/weizmann_scripts/run_alphafold_multimer_msa_genration_single_time.sh
JOB_MEMORY_MB=100000

bsub -q new-short -R rusage[mem="$JOB_MEMORY_MB"] -oo "$JOB_LOGS_DIR" bash "$MSA_GENERATION_SCRIPT" "$HOST_PROTEIN" "$VIRUS_PROTEIN" "$RESULTS_DIR"