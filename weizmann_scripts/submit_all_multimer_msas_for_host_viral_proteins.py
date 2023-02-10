"""
this script calls alphafold multimer script with only msa generation and saves the MSAs to the configurable places
"""
import os
import shutil
from itertools import zip_longest
from pathlib import Path
from typing import List

from data_handaling import uniprot
from data_handaling.hvidb import get_hvidb_from_csv
from weizmann_scripts import weizmann_config
from weizmann_scripts.data_organization.prepare_result_dir_for_alphafold_on_hvidb import main as prepare_results_dir

target_host_proteins_dir = weizmann_config.HUMAN_PROTEINS_DIR
target_viral_proteins_dir = weizmann_config.VIRUS_PROTEINS_DIR

tmp_results_dir = weizmann_config.TMP_DIR


def get_proteins_to_calculate_masa_from_hvidb() -> (List[str], List[str]):
    hvidb_filtered = get_hvidb_from_csv(weizmann_config.HVIDB_FILTERED_CSV_PATH)
    unique_human_uniprot_ids = hvidb_filtered.df[hvidb_filtered.columns_names.uniprot_human].unique()
    unique_virus_uniprot_ids = hvidb_filtered.df[hvidb_filtered.columns_names.uniprot_virus].unique()

    return list(unique_human_uniprot_ids), list(unique_virus_uniprot_ids)


def copy_msas_to_permenant_dir(msas_results_dir: Path, human_prots_dir: Path, human_prot_name: str,
                               virus_prots_dir: Path, virus_prot_name: str):
    human_msa_src_dir = Path(msas_results_dir, "A")
    virus_msa_src_dir = Path(msas_results_dir, "B")

    human_msa_dest_dir = Path(human_prots_dir, human_prot_name, "msas", "A")
    virus_msa_dest_dir = Path(virus_prots_dir, virus_prot_name, "msas", "B")

    if not human_msa_dest_dir.exists():
        shutil.copytree(human_msa_src_dir, human_msa_dest_dir)
    if not virus_msa_dest_dir.exists():
        shutil.copytree(virus_msa_src_dir, virus_msa_dest_dir)


host_proteins, virus_proteins = get_proteins_to_calculate_masa_from_hvidb()
host_proteins = [uniprot.transform_domain_id_to_protein_id(name) for name in host_proteins]
virus_proteins = [uniprot.transform_domain_id_to_protein_id(name) for name in virus_proteins]
fill_value = virus_proteins[0] if len(host_proteins) > len(virus_proteins) else host_proteins[0]

proteins_complexes = list(zip_longest(host_proteins, virus_proteins, fillvalue=fill_value))

limit_num_of_jobs = 3
start_job = 0
problematic_protein = "Q15418"
proteins_complexes = [proteins_complexes[[human_prot for human_prot, _ in proteins_complexes].index("Q15418")]]
for human_prot_name, virus_prot_name in list(proteins_complexes)[start_job:start_job + limit_num_of_jobs]:
    os.environ["RESULTS_DIR"] = str(tmp_results_dir)
    os.environ["HOST_PROTEIN_NAME"] = human_prot_name
    os.environ["VIRUS_PROTEIN_NAME"] = virus_prot_name
    try:
        prepare_results_dir()
        os.system(
            f"bash submit_single_multimer_msa_generation.sh {human_prot_name} {virus_prot_name} {str(tmp_results_dir)}")
    except FileNotFoundError as e:

        print(f"\none of {human_prot_name} or {virus_prot_name}, probably didnt have fasta from uni prot")
        print(str(e))
