from typing import Dict

import numpy as np
import pandas as pd

from results_visualization.results_loading import MultiModelResults, AfModelResultsKeys

AGGREGATIONS = {"mean": np.mean, "max": np.max, "median": np.median}


def aggregate_ptm_iptm(all_results: Dict[str, MultiModelResults]) -> pd.DataFrame:
    results_keys = AfModelResultsKeys()

    # NOTE if you want to add metric you need to add to both columns and protein unpacking loop
    columns = []
    for agg_func_name in AGGREGATIONS:
        columns.append(f"{agg_func_name}_{results_keys.ptm}")
        columns.append(f"{agg_func_name}_{results_keys.iptm}")
    aggregated_metrics = {}
    for protein_name, multi_model_results in all_results.items():
        aggregated_values = []
        for agg_func_name, agg_func in AGGREGATIONS.items():
            aggregated_values.append(agg_func(multi_model_results.get_all_ptms()))
            aggregated_values.append(agg_func(multi_model_results.get_all_iptms()))
        aggregated_metrics[protein_name] = tuple(aggregated_values)

    return pd.DataFrame.from_dict(aggregated_metrics, orient="index",
                                  columns=columns)
