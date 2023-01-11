import argparse
import os
import shutil
from pathlib import Path

from tqdm import tqdm

from weizmann_scripts import weizmann_config


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="copy all msas of miltimer prediction dir,"
                    " after the copy will delete the source msas and create symbolic links")

    # required inputes
    parser.add_argument('--results_dir', type=str)
    parser.add_argument('--host_proteins_dir', type=str, default=weizmann_config.HUMAN_PROTEINS_DIR)
    parser.add_argument('--virus_proteins_dir', type=str, default=weizmann_config.VIRUS_PROTEINS_DIR)

    # configurations
    parser.add_argument('--create_symlink', type=bool, default=True)

    arguments = parser.parse_args()
    return arguments


def copy_msas_from_results_dir_and_replace_with_link(results_dir: str, host_protein_dir: str, virus_protein_dir: str,
                                                     create_symlink: bool):
    results_dir_name_split = Path(results_dir).stem.split(sep="_")
    host_protein_name, virus_protein_name = results_dir_name_split[0], "_".join(results_dir_name_split[1:])
    src_msas_dir = Path(results_dir, "msas")
    host_src_msas_dir = Path(src_msas_dir, "A")
    virus_src_msas_dir = Path(src_msas_dir, "B")

    host_dest_msas_dir = Path(host_protein_dir, host_protein_name, "msas", "A")
    virus_dest_msas_dir = Path(virus_protein_dir, virus_protein_name, "msas", "B")

    if host_src_msas_dir.exists():
        _copy_src_dir_to_dest_and_replace_src_with_link_to_dst(create_symlink, host_src_msas_dir, host_dest_msas_dir)
    if virus_src_msas_dir.exists():
        _copy_src_dir_to_dest_and_replace_src_with_link_to_dst(create_symlink, virus_src_msas_dir, virus_dest_msas_dir)


def _copy_src_dir_to_dest_and_replace_src_with_link_to_dst(create_symlink, src_dir, dest_dir):
    if not dest_dir.exists():
        shutil.copytree(src_dir, dest_dir)
    if not src_dir.is_symlink():
        shutil.rmtree(src_dir)
        if create_symlink:
            os.symlink(dest_dir, src_dir)



if __name__ == '__main__':
    args = parse_arguments()
    if Path(args.results_dir, "msas").exists():
        copy_msas_from_results_dir_and_replace_with_link(results_dir=args.results_dir,
                                                         host_protein_dir=args.host_proteins_dir,
                                                         virus_protein_dir=args.virus_proteins_dir,
                                                         create_symlink=args.create_symlink)
    for sub_dir in tqdm(Path(args.results_dir).glob("*")):
        if sub_dir.is_dir() and Path(sub_dir, "msas").exists():
            copy_msas_from_results_dir_and_replace_with_link(results_dir=str(sub_dir),
                                                             host_protein_dir=args.host_proteins_dir,
                                                             virus_protein_dir=args.virus_proteins_dir,
                                                             create_symlink=args.create_symlink)
