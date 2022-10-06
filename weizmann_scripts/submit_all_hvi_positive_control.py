import os

import pandas as pd
from data_handaling import hvidb
import weizmann_config

positive_control_hvidb = hvidb.HvidbDataset(pd.read_csv(weizmann_config.HVIDV_POSITIVE_CONTROL_CSV_PATH))

for index, row in positive_control_hvidb.df.iterrows():
    host_protein = row[positive_control_hvidb.columns_names.uniprot_human]
    virus_protein = row[positive_control_hvidb.columns_names.uniprot_virus]

    os.system(f"bash submit_job_single_multimer_run.sh {host_protein} {virus_protein}")