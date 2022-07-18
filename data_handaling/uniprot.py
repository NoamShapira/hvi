import os
import shutil
from io import StringIO
from pathlib import Path
from typing import List, Dict, Optional

import requests as r
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from tqdm.contrib.concurrent import thread_map

from data_handaling.fasta_handaling import write_fastas_to_files
from weizmann_scripts.weizmann_config import HVI_DATA_DIR


def _get_single_sequence_from_uniprot(cID: str) -> Optional[SeqRecord]:
    baseUrl = "http://www.uniprot.org/uniprotkb/"
    currentUrl = baseUrl + cID + ".fasta"
    response = r.post(currentUrl)
    cData = ''.join(response.text)
    Seq = StringIO(cData)
    pSeq = list(SeqIO.parse(Seq, 'fasta'))
    return pSeq[0] if len(pSeq) > 0 else None


def get_protein_sequences(uniprot_list: List[str]) -> Dict[str, SeqRecord]:
    pSeqs = {}
    sequences_list = thread_map(_get_single_sequence_from_uniprot, uniprot_list,
                               desc="loading sequences from uniprot",
                               unit="protein")
    for name, seq in zip(uniprot_list, sequences_list):
        if seq is not None:
            pSeqs[name] = seq
    return pSeqs


if __name__ == '__main__':
    seqs_dict = get_protein_sequences(['Q93009', 'F5HF68'])
    write_fastas_to_files(list(seqs_dict.keys()), list(seqs_dict.values()), Path(HVI_DATA_DIR, "tests"))

    assert Path(HVI_DATA_DIR, "tests", "Q93009", "Q93009.fasta").exists()

    shutil.rmtree(Path(HVI_DATA_DIR, "tests", "Q93009"))
    shutil.rmtree(Path(HVI_DATA_DIR, "tests", "F5HF68"))