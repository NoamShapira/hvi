from data_handaling import hvidb, uniprot
from data_handaling.fasta_handaling import write_fastas_to_files
from weizmann_scripts import weizmann_config

hvidb = hvidb.get_hvidb_from_csv(weizmann_config.HVIDB_FILTERED_CSV_PATH)

all_human_protein_uniprot_ids = list(set(hvidb.df[hvidb.columns_names.uniprot_human].values))
all_viral_protein_uniprot_ids = list(set(hvidb.df[hvidb.columns_names.uniprot_virus].values))

# all_human_protein_uniprot_ids = [prot_name for prot_name in all_human_protein_uniprot_ids if "PRO" in prot_name]
# all_viral_protein_uniprot_ids = [prot_name for prot_name in all_viral_protein_uniprot_ids if "PRO" in prot_name]

all_human_protein_uniprot_ids = list(map(uniprot.transform_domain_id_to_protein_id, all_human_protein_uniprot_ids))
all_viral_protein_uniprot_ids = list(map(uniprot.transform_domain_id_to_protein_id, all_viral_protein_uniprot_ids))

all_human_sequences_dict = uniprot.get_protein_sequences(all_human_protein_uniprot_ids)
all_viral_sequences_dict = uniprot.get_protein_sequences(all_viral_protein_uniprot_ids)

write_fastas_to_files(list(all_human_sequences_dict.keys()), list(all_human_sequences_dict.values()),
                      weizmann_config.HUMAN_PROTEINS_DIR)
write_fastas_to_files(list(all_viral_sequences_dict.keys()), list(all_viral_sequences_dict.values()),
                      weizmann_config.VIRUS_PROTEINS_DIR)
