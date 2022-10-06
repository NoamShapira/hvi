from data_handaling.hvidb import get_hvidb_from_csv
import weizmann_config

hvidb = get_hvidb_from_csv(weizmann_config.HVIDV_CSV_PATH)

filtered_hvidb_df = hvidb.df
filtered_hvidb_df = filtered_hvidb_df[filtered_hvidb_df[hvidb.columns_names.experimental_system] == "pull down"]
filtered_hvidb_df = filtered_hvidb_df[
    filtered_hvidb_df.apply(lambda row: row[hvidb.columns_names.interaction_type] == "direct interaction", axis=1)]

filtered_hvidb_df.to_csv(weizmann_config.HVIDV_POSITIVE_CONTROL_CSV_PATH)
