import json
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Tuple, List, Dict, Optional, NamedTuple

import numpy as np
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map


class AfModelResultsKeys(NamedTuple):
    iptm = "iptm"
    ptm = "ptm"
    pae = "predicted_aligned_error"
    plddt = "plddt"


@dataclass
class ModelResults:
    model_name: str
    pae: Optional[np.array]
    plddt: np.array
    ptm: int
    iptm: int


@dataclass
class MultiModelResults:
    results_list: List[ModelResults]
    model_names_ordered_by_ranks: List[str]
    chains_lengths: Optional[List[int]] = None

    @property
    def num_models(self) -> int:
        return len(self.results_list)

    def get_all_paes(self) -> List:
        return [model_results.pae for model_results in self.results_list]

    def get_all_plddts(self) -> List:
        return [model_results.plddt for model_results in self.results_list]

    def get_all_ptms(self) -> List:
        return [model_results.ptm for model_results in self.results_list]

    def get_all_iptms(self) -> List:
        return [model_results.iptm for model_results in self.results_list]

    def get_results_of_best_model_according_to_alphafold(self) -> ModelResults:
        best_model_name = self.model_names_ordered_by_ranks[0]
        for model_results in self.results_list:
            if model_results.model_name == best_model_name:
                return model_results


def get_results_from_alphafold_results_dir(path: Union[Path, str]) -> MultiModelResults:
    all_model_results = []
    results_keys = AfModelResultsKeys()
    with open(f"{path}/ranking_debug.json", 'r') as f:
        ranks = json.load(f)["order"]

    for model_name in ranks:
        try:
            with open(f"{path}/result_{model_name}.pkl", 'rb') as f:
                data = pickle.load(f)
            pae = data[results_keys.pae] if results_keys.pae in data else None
            plddt = data[results_keys.plddt]
            ptm = (data[results_keys.ptm])
            iptm = (data[results_keys.iptm])
            all_model_results.append(ModelResults(pae=pae, plddt=plddt, ptm=ptm, iptm=iptm, model_name=model_name))
        except FileNotFoundError:
            # model was calculated but results are not saved
            pass
    if len(all_model_results) == 0:
        raise ValueError(f"in the path: {path} all results are deleted")

    if os.path.isfile(f"{path}/msas/chain_id_map.json"):
        with open(f"{path}/msas/chain_id_map.json", 'r') as f:
            chains = json.load(f)
        print(f"Found {str(len(chains))} chains, in {path.name}")
        lengths_of_proteins = []
        for chain_key, chain_data in chains.items():
            # full_sequence_description = chains[chain_key]["description"]
            # seq_name = full_sequence_description.split('|')[1] if '|' in full_sequence_description else chain_key
            lengths_of_proteins.append(len(chain_data["sequence"]))
    else:
        print(f"Found 1 chain, in {path.name}")
        lengths_of_proteins = None

    return MultiModelResults(results_list=all_model_results, model_names_ordered_by_ranks=ranks,
                             chains_lengths=lengths_of_proteins)


def _load_name_and_metrics_from_path(path: Path) -> Tuple[str, Optional[MultiModelResults]]:
    prediction_name = path.name
    try:
        model_results = get_results_from_alphafold_results_dir(path)
    except FileNotFoundError:
        model_results = None
    return prediction_name, model_results


def load_metrics_from_multiple_dirs(paths: List[Path], num_workers=8) -> Dict[str, Optional[MultiModelResults]]:
    all_metrics_as_tuples = process_map(_load_name_and_metrics_from_path, paths,
                                        max_workers=num_workers)
    return {name: model_results for name, model_results in all_metrics_as_tuples if model_results is not None}


if __name__ == '__main__':
    dir_with_all_results_dirs = Path(r"/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold")
    paths_of_all_results_dirs = [Path(dir_entry.path) for dir_entry in os.scandir(dir_with_all_results_dirs) if
                                 dir_entry.is_dir()]
    # multi_model_results = get_results_from_alphafold_results_dir(paths_of_all_results_dirs[0])
    for complex_path in tqdm(paths_of_all_results_dirs):
        try:
            with open(f"{complex_path}/ranking_debug.json", 'r') as f:
                ranks = json.load(f)["order"]
                for i, model_name in enumerate(ranks):
                    if i != 0:
                        os.remove(f"{complex_path}/result_{model_name}.pkl")
        except FileNotFoundError:
            pass


