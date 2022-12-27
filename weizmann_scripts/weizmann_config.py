from pathlib import Path

SOREK_LAB_PATH = Path("/home/labs/sorek")

# lab bacteria phage database
EREZ_DATA_DIR = Path(SOREK_LAB_PATH, "erezy/AF")
EREZ_BACTERIA_PATH = Path(EREZ_DATA_DIR, "matrix/bacteria")
EREZ_PHAGE_PATH = Path(EREZ_DATA_DIR, "matrix/phages")

# human virus ppi data
HVI_DIR = Path(SOREK_LAB_PATH, "noamsh/human_virus_interactions")
HVI_DATA_DIR = Path(HVI_DIR, "data")
HUMAN_PROTEINS_DIR = Path(HVI_DATA_DIR, "human_proteins")
VIRUS_PROTEINS_DIR = Path(HVI_DATA_DIR, "virus_proteins")
HVIDB_CSV_PATH = Path(HVI_DATA_DIR, "HVIDB_PPIs.csv")
HVIDB_POSITIVE_CONTROL_CSV_PATH = Path(HVI_DATA_DIR, "HVIDB_PPIs_positive_control.csv")
HVIDB_FILTERED_CSV_PATH = Path(HVI_DATA_DIR, "human_viruses_filtered.csv")

# personal directories
IMAGES_DIR = Path(SOREK_LAB_PATH, "noamsh/AF_multimer_exercise/images")
TMP_DIR = Path(HVI_DATA_DIR, "tests", "tmp")

