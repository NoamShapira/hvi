from pathlib import Path
from typing import NamedTuple

import pandas as pd


class HvidbColumnNames(NamedTuple):
    uniprot_human = "Uniprot_human"
    uniprot_virus = "Uniprot_virus"
    organism_virus = "Organism_virus"
    interaction_type = "Interaction_Type"
    organism_interactor_virus = "Organism_Interactor_virus"
    has_complex_structure = "Complex_structure"
    viral_family = "Viral_family"
    human_gene_name = "Human_GeneName"
    human_protein_name = "Human_ProteinName"
    virus_gene_name = "Virus_GeneName"
    virus_protein_name = "Virus_ProteinName"


class HvidbDataset:
    def __init__(self, df: pd.DataFrame):
        self.columns_names = HvidbColumnNames()
        self.df = df


def get_hvidb_from_csv(csv_path: Path) -> HvidbDataset:
    return HvidbDataset(pd.read_csv(csv_path))
