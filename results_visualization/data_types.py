from typing import NamedTuple


class AfModelResultsKeys(NamedTuple):
    iptm = "iptm"
    ptm = "ptm"
    pae = "predicted_aligned_error"
    plddt = "plddt"