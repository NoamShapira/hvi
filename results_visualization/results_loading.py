import json
import os
import pickle
from pathlib import Path
from typing import Union, Tuple, List, Dict

import numpy as np
import pandas as pd

from results_visualization.data_types import AfModelResultsKeys


def get_metrics_from_alphafold_results_dir(path: Union[Path, str]) -> Tuple[List, List, List, List]:
    paes = []
    plddts = []
    ptms = []
    iptms = []
    results_keys = AfModelResultsKeys()
    with open(f"{path}/ranking_debug.json", 'r') as f:
        ranks = json.load(f)["order"]
    for model_name in ranks:
        with open(f"{path}/result_{model_name}.pkl", 'rb') as f:
            data = pickle.load(f)
        if "predicted_aligned_error" in data:
            paes.append(data[results_keys.pae])
        plddts.append(data[results_keys.plddt])
        ptms.append((data[results_keys.ptm]))
        iptms.append((data[results_keys.iptm]))

    return paes, plddts, ptms, iptms

def load_metrics_from_multiple_dirs(paths: List[Path]) -> Dict[str, Tuple[List, List, List, List]]:
    all_metrics = dict()
    for path in paths:
        prediction_name = path.name
        all_metrics[prediction_name] = get_metrics_from_alphafold_results_dir(path)
    return all_metrics

def aggregate_ptm_iptm(all_metrics: Dict[str, Tuple[List, List, List, List]]) -> pd.DataFrame:
    results_keys = AfModelResultsKeys()
    aggregations = {"mean": np.mean, "max": np.max}
    # NOTE if you want to add metric you need to add to obthe columns and protein unpackong loop
    columns = []
    for agg_func_name in aggregations:
        columns.append(f"{agg_func_name}_{results_keys.ptm}")
        columns.append(f"{agg_func_name}_{results_keys.iptm}")
    aggregated_metrics= {}
    for protein_name , (_, _, ptms, iptms) in all_metrics.items():
        aggregated_values = []
        for agg_func_name , agg_func in aggregations.items():
            aggregated_values.append(agg_func(ptms))
            aggregated_values.append(agg_func(iptms))
        aggregated_metrics[protein_name] = tuple(aggregated_values)

    return pd.DataFrame.from_dict(aggregated_metrics, orient="index",
                                  columns=columns)

if __name__ == '__main__':
    dir_with_all_results_dirs = Path(r"/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold")
    paths_of_all_results_dirs = [Path(dir_entry.path) for dir_entry in os.scandir(dir_with_all_results_dirs) if
                                 dir_entry.is_dir()]
    all_results_dict = load_metrics_from_multiple_dirs(paths_of_all_results_dirs)
    df = pd.DataFrame.from_dict(all_results_dict, orient='index')

