import json
# from Bio import AlignIO
import os
from functools import partial
from pathlib import Path
from string import ascii_uppercase, ascii_lowercase

import matplotlib.pyplot as plt
import numpy as np
from tqdm.contrib.concurrent import process_map

from results_visualization.results_loading import get_metrics_from_alphafold_results_dir

plt.switch_backend('Agg')


def plot_and_save_plddts(plddts, out_path, return_figure, Ls=None, dpi=300, fig=True):
    if fig: plt.figure(figsize=(8, 5), dpi=100)
    plt.title("Predicted lDDT per position")
    for n, plddt in enumerate(plddts):
        plt.plot(plddt, label=f"rank_{n + 1}")
    if Ls is not None:
        L_prev = 0
        for L_i in Ls[:-1]:
            L = L_prev + L_i
            L_prev += L_i
            plt.plot([L, L], [0, 100], color="black")
    plt.legend()
    plt.ylim(0, 100)
    plt.ylabel("Predicted lDDT")
    plt.xlabel("Positions")
    plt.savefig(out_path)
    if return_figure:
        return fig
    else:
        plt.close()


def plot_and_save_paes(paes, out_path, return_figure, Ls=None, dpi=300, fig=True):
    num_models = len(paes)
    if fig: plt.figure(figsize=(3 * num_models, 2), dpi=dpi)
    for n, pae in enumerate(paes):
        plt.subplot(1, num_models, n + 1)
        plt.title(f"rank_{n + 1}")
        Ln = pae.shape[0]
        plt.imshow(pae, cmap="bwr", vmin=0, vmax=30, extent=(0, Ln, Ln, 0))
        if Ls is not None and len(Ls) > 1: plot_ticks(Ls)
        plt.colorbar()
    plt.savefig(out_path)
    if return_figure:
        return fig
    else:
        plt.close()


def plot_ticks(Ls):
    alphabet_list = list(ascii_uppercase + ascii_lowercase)

    Ln = sum(Ls)
    L_prev = 0
    for L_i in Ls[:-1]:
        L = L_prev + L_i
        L_prev += L_i
        plt.plot([0, Ln], [L, L], color="black")
        plt.plot([L, L], [0, Ln], color="black")
    ticks = np.cumsum([0] + Ls)
    ticks = (ticks[1:] + ticks[:-1]) / 2
    plt.yticks(ticks, alphabet_list[:len(ticks)])


def create_plddts_and_paes_images_in_alphafold_results_dir(results_path: Path, images_dir_path: Path = None):
    try:
        if os.path.isfile(f"{results_path}/msas/chain_id_map.json"):
            with open(f"{results_path}/msas/chain_id_map.json", 'r') as f:
                chains = json.load(f)
            print(f"Found {str(len(chains))} chains, in {results_path.name}")
            lengths_of_proteins = [len(chain_data["sequence"]) for chain_key, chain_data in chains.items()]
        else:
            print(f"Found 1 chain, in {results_path.name}")
            lengths_of_proteins = None

        paes, plddts, _, _ = get_metrics_from_alphafold_results_dir(results_path)
        print(f"loaded paes and plddts, from {results_path.name}")

        images_dir_path = f"{results_path}/images" if images_dir_path is None else images_dir_path
        if not os.path.exists(images_dir_path):
            os.mkdir(images_dir_path)
        if len(paes) > 0:
            plot_and_save_paes(paes, f"{images_dir_path}/{results_path.name}_pae.png", return_figure=False, Ls=lengths_of_proteins)
        plot_and_save_plddts(plddts, f"{images_dir_path}/{results_path.name}_plddt.png", return_figure=False, Ls=lengths_of_proteins)
        print(f"saved images to {images_dir_path}")
    except FileNotFoundError:
        print(f"{results_path} does not contains full alphafold results")


if __name__ == '__main__':
    # run on single results file
    # # results_path = sys.argv[1]
    # alphafold_results_path = r"/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold/O43143_P04608"
    #
    # alphafold_results_path = Path(alphafold_results_path)
    # create_plddts_and_paes_images_in_alphafold_results_dir(alphafold_results_path)

    dir_with_all_results_dirs = Path(r"/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold")
    images_dir = Path(r"/home/labs/sorek/noamsh/human_virus_interactions/results/alphafold_images")
    # images_dir = None # defualt behavior will create images inside the result dirs
    paths_of_all_results_dirs = [Path(dir_entry.path) for dir_entry in os.scandir(dir_with_all_results_dirs) if
                                 dir_entry.is_dir()]
    process_map(partial(create_plddts_and_paes_images_in_alphafold_results_dir, images_dir_path=images_dir),
                paths_of_all_results_dirs,
                max_workers=16)
