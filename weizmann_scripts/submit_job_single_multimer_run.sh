#HOST_PROTEIN="LsoA" # short defence protein - for IMG-VR
#HOST_PROTEIN="S6B2B6" #  interacts with Q2N0S6 - for HVIDB
#HOST_PROTEIN="P78310" #  interacts with P36711 - for HVIDB with solved interaction structure
HOST_PROTEIN=${1:-"P78310"}

#VIRUS_PROTEIN="LAB1717" # has interaction with LsoA- for IMG-VR
#VIRUS_PROTEIN="Q2N0S6" # has interaction with S6B2B6 - for HVIDB
#VIRUS_PROTEIN="P36711" # has interaction with P78310 - for HVIDB with solved interaction structure
VIRUS_PROTEIN=${2:-"P36711"}

VAR=${1:-DEFAULTVALUE}

JOB_LOGS_DIR=/home/labs/sorek/noamsh/wexac_job_logs/"${HOST_PROTEIN}_${VIRUS_PROTEIN}"
mkdir -p "$JOB_LOGS_DIR"

PIPELINE_SCRIPT=/home/labs/sorek/noamsh/human_virus_interactions/hvi/weizmann_scripts/run_multimer_single_time.sh
JOB_MEMORY_MB=100000

bsub -q gpu-short -R rusage[mem="$JOB_MEMORY_MB"] -gpu num=1 -oo "$JOB_LOGS_DIR" -R 'hname!=cn300 && hname!=cn301 && hname!=cn302 && hname!=cn303 && hname!=cn304 && hname!=cn736' bash "$PIPELINE_SCRIPT" "$HOST_PROTEIN" "$VIRUS_PROTEIN"
