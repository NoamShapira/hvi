"""
this script will repeat te filtering that was done with Rotem on the hvidb
 according to experimental type
this is mainly for documentation and reproducability because the exel that we created is also available.
If this script will run it will not override the original but create a .csv file
"""
from typing import Optional

from data_handaling.hvidb import get_hvidb_from_csv
from weizmann_scripts import weizmann_config

hvidb = get_hvidb_from_csv(weizmann_config.HVIDB_CSV_PATH)
filtered_hvidb_df = hvidb.df

allowed_experimental_system = ["pull down", "affinity chromatography technology", "coimmunoprecipitation",
                               "x-ray crystallography","affinity purification-mass spectrometry",
                               # "x-ray crystallography*","pull down*",
                               # "coimmunoprecipitation*", "mic tag coimmunoprecipitation",
                               # "immunodepleted coimmunoprecipitation", "anti tag coimmunoprecipitation"
                               ]


def any_allowed_experimental_system(all_systems: Optional[str]) -> bool:
    if not isinstance(all_systems, str):
        return False
    # all_systems_split = all_systems.split(",")
    return any([system_name in all_systems for system_name in allowed_experimental_system])


filtered_hvidb_df = filtered_hvidb_df[
    filtered_hvidb_df.apply(lambda row: any_allowed_experimental_system(row[hvidb.columns_names.experimental_system]),
                            axis=1)]

filtered_hvidb_df.to_csv(weizmann_config.HVIDB_FILTERED_CSV_PATH)
