#HOST_PROTEIN="LsoA" # short defence protein - for IMG-VR
HOST_PROTEIN="S6B2B6" #  interacts with Q2N0S6	- for HVIDB

#VIRUS_PROTEIN="IMGVR2400828" # first phage protien - for IMG-VR
#VIRUS_PROTEIN="LAB1717" # has interaction with LsoA- for IMG-VR
VIRUS_PROTEIN="Q2N0S6" # has interaction with S6B2B6	- for HVIDB

JOB_LOGS_DIR=/home/labs/sorek/noamsh/wexac_job_logs
mkdir -p "$JOB_LOGS_DIR"

PIPELINE_SCRIPT=/home/labs/sorek/noamsh/human_virus_interactions/hvi/weizmann_scripts/run_multimer_single_time.sh
JOB_MEMORY_MB=40000

bsub -q gpu-long -R rusage[mem="$JOB_MEMORY_MB"] -gpu num=1 -o "$JOB_LOGS_DIR" -R 'hname!=cn300 && hname!=cn301 && hname!=cn302 && hname!=cn303 && hname!=cn304 && hname!=cn736' bash "$PIPELINE_SCRIPT" "$HOST_PROTEIN" "$VIRUS_PROTEIN"
