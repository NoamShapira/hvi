from pathlib import Path

SOREK_LAB_PATH = Path("/home/labs/sorek")

# lab bacteria phage database
EREZ_DATA_DIR = Path(SOREK_LAB_PATH, "erezy/AF")
EREZ_BACTERIA_PATH = Path(EREZ_DATA_DIR, "matrix/bacteria")
EREZ_PHAGE_PATH = Path(EREZ_DATA_DIR, "matrix/phages")

# human virus ppi
HVI_DATA_DIR = Path(SOREK_LAB_PATH, "noamsh/human_virus_interactions/data")
HUMAN_PROTEINS_DIR = Path(HVI_DATA_DIR, "human_proteins")
VIRUS_PROTEINS_DIR = Path(HVI_DATA_DIR, "virus_proteins")
HVIDV_CSV_PATH = Path(HVI_DATA_DIR, "HVIDB_PPIs.csv")

# personal directories
IMAGES_DIR = Path(SOREK_LAB_PATH, "noamsh/AF_multimer_exercise/images")

