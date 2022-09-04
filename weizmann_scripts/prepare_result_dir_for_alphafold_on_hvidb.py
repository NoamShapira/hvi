import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.append('/home/labs/sorek/noamsh/human_virus_interactions/hvi')

from data_handaling.fasta_handaling import concatenate_muiltiple_fasta_to_one_fasta
import weizmann_scripts.weizmann_config as weizmann_config

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="creating results directory like alphafold expect to enable pre-computation of msas")

    # required inputes
    parser.add_argument('--results_dir', type=str)
    parser.add_argument('--host_protein_name', type=str)
    parser.add_argument('--virus_protein_name', type=str)

    # configurations
    parser.add_argument('--host_proteins_dir', type=str, default=str(weizmann_config.HUMAN_PROTEINS_DIR))
    parser.add_argument('--virus_proteins_dir', type=str, default=str(weizmann_config.VIRUS_PROTEINS_DIR))

    parser.add_argument("--fasta_complex_format", type=str, default="alphafold", choices=["alphafold", "colabfold"])

    arguments = parser.parse_args()
    return arguments


def _parse_args_to_combined_protein_name(args) -> str:
    return f"{args.host_protein_name}_{args.virus_protein_name}"


def create_combined_result_dir_with_fasta(args):
    host_fasta_path = Path(args.host_proteins_dir, args.host_protein_name,
                           f"{args.host_protein_name}.fasta")
    virus_fasta_path = Path(args.virus_proteins_dir, args.virus_protein_name, f"{args.virus_protein_name}.fasta")
    new_combined_dir_path = Path(args.results_dir, f"{_parse_args_to_combined_protein_name(args)}")
    new_combined_fasta_path = Path(new_combined_dir_path, f"{_parse_args_to_combined_protein_name(args)}.fasta")

    if not new_combined_dir_path.exists():
        os.mkdir(new_combined_dir_path)
    if not new_combined_fasta_path.exists():
        concatenate_muiltiple_fasta_to_one_fasta(input_fastas_paths=[host_fasta_path, virus_fasta_path],
                                                 output_fasta=new_combined_fasta_path,
                                                 fasta_format=args.fasta_complex_format)


def copy_msas_if_exist_to_dir(args, prefix_to_add_to_protein_name=""):
    """acording to alphafold nameing conventions, and erez matrix folder conventions"""
    dest_msas_dir_path = Path(args.results_dir,
                              f"{prefix_to_add_to_protein_name}{_parse_args_to_combined_protein_name(args)}", "msas")
    dest_host_msas_dir = Path(dest_msas_dir_path, "A")
    dest_virus_msas_dir = Path(dest_msas_dir_path, "B")

    host_msas_existing_dir = Path(args.host_proteins_dir, args.host_protein_name, "msas", "A")
    if host_msas_existing_dir.exists() and not dest_host_msas_dir.exists():
        shutil.copytree(host_msas_existing_dir, dest_host_msas_dir)

    virus_msas_existing_dir = Path(args.virus_proteins_dir, args.virus_protein_name, "msas", "B")
    if virus_msas_existing_dir.exists() and not dest_virus_msas_dir.exists():
        shutil.copytree(virus_msas_existing_dir, dest_virus_msas_dir)

if __name__ == '__main__':
    arguments = parse_arguments()
    create_combined_result_dir_with_fasta(arguments)
    copy_msas_if_exist_to_dir(arguments)
