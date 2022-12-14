from statistics import harmonic_mean
from typing import Dict, Tuple, Callable, List

import numpy as np
import pandas as pd

from results_visualization.ptm_iptm_analyzer import AGGREGATIONS
from results_visualization.results_loading import MultiModelResults, ModelResults


def aggregate_plddt(all_results: Dict[str, MultiModelResults]) -> Dict[str, Dict[str, Tuple[np.array, float]]]:
    aggregated_plddt = {}
    for protein_name, multi_model_results in all_results.items():
        metrics_dict = {}
        for agg_func_name, agg_func in AGGREGATIONS.items():
            combined_plddt = agg_func(np.vstack(multi_model_results.get_all_plddts()), axis=0)
            metrics_dict[agg_func_name] = combined_plddt, agg_func(combined_plddt)
        aggregated_plddt[protein_name] = metrics_dict
    return aggregated_plddt


def convert_plddt_results_to_df(plddt_aggregated_results: Dict[str, Dict[str, Tuple[np.array, float]]]) -> pd.DataFrame:
    aggregated_scalar_metrics = {}
    columns = list(AGGREGATIONS.keys())
    for prot_name, prot_metrics in plddt_aggregated_results.items():
        scalar_metrics = [prot_metrics[col][1] for col in columns]
        aggregated_scalar_metrics[prot_name] = scalar_metrics
    return pd.DataFrame.from_dict(aggregated_scalar_metrics, orient="index",
                                  columns=columns)


def _split_plddt_according_to_sequence_lengths(plddt: np.ndarray, sequences_lengths: List[int]) -> List[np.ndarray]:
    assert sum(sequences_lengths) == len(plddt), \
        "plddts should be the length of all the sequences combined"
    sequences_ind_ranges = []
    cur_start_ind = 0
    for sequences_length in sequences_lengths:
        cur_end_ind =  cur_start_ind + sequences_length
        sequences_ind_ranges.append((cur_start_ind, cur_end_ind))
        cur_start_ind = cur_end_ind

    plddts = []
    for start_ind, end_ind in sequences_ind_ranges:
        plddts.append(plddt[start_ind:end_ind])
    return plddts


def aggregate_plddt_per_sequence(model_results: ModelResults, sequences_lengths: List[int],
                                 agg_func: Callable = np.mean) -> List[int]:
    splitted_plddts = _split_plddt_according_to_sequence_lengths(model_results.plddt, sequences_lengths)
    aggregated_plddt = list(map(agg_func, splitted_plddts))
    return aggregated_plddt


def get_best_model_according_to_per_sequence_plddt(all_model_results: MultiModelResults) -> Tuple[ModelResults,
                                                                                                  int, List[int]]:
    best_model_results, best_overall_results, best_aggregated_plddts_of_different_chains = None, None, None
    for model_results in all_model_results.results_list:
        aggregated_plddts_of_different_chains = aggregate_plddt_per_sequence(model_results, all_model_results.chains_lengths)
        overall_plddt_score = harmonic_mean(aggregated_plddts_of_different_chains)
        if best_overall_results is None or overall_plddt_score > best_overall_results:
            best_overall_results = overall_plddt_score
            best_aggregated_plddts_of_different_chains = aggregated_plddts_of_different_chains
            best_model_results = model_results

    return best_model_results, best_overall_results, best_aggregated_plddts_of_different_chains


def get_interaction_metrics() -> pd.DataFrame:
    """

    :return: dataframe
    index is Protein Iteraction Name
    columns:
        - A_prot_name: str
        - B_prot_name: str
        - total_plddt: 1d np.array
        - A_plddt: 1d np.array
        - B_plddt: 1d np.array
        - A_length: int
        - B_length: int
        - A_mean_plddt: float
        - B_mean_plddt: float
        - F_score_mean_plddt: float n8
    """

    raise NotImplementedError
