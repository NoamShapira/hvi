import os
from pathlib import Path
from typing import List

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm


def write_fastas_to_files(protein_names: List[str], proteins_seqs: List[SeqRecord], output_dir: Path):
    if not output_dir.exists():
        os.mkdir(output_dir)

    for name, seq in tqdm(zip(protein_names, proteins_seqs), desc=f"writing fastas to dir {output_dir}"):
        protein_output_dir = Path(output_dir, name)
        if not protein_output_dir.exists():
            os.mkdir(protein_output_dir)
        fasta_path = Path(protein_output_dir, f"{name}.fasta")
        if not fasta_path.exists():
            SeqIO.write(seq, fasta_path, "fasta")


def _concatenate_multiple_files_to_one_file(src_files: List[Path], dst_path: Path):
    with open(dst_path, 'w+') as outfile:
        for file_path in src_files:
            with open(file_path) as infile:
                outfile.write(infile.read())


def concatenate_muiltiple_fasta_to_one_fasta(input_fastas_paths: List[Path], output_fasta: Path, fasta_format: str):
    if fasta_format == "alphafold":
        _concatenate_multiple_files_to_one_file(input_fastas_paths, output_fasta)
    elif fasta_format == "colabfold":
        raise NotImplementedError
    else:
        raise ValueError("fasta_format should be from [alphafold, colabfold]")
