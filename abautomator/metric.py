from dataclasses import dataclass

import pandas as pd

@dataclass
class Metric:
    name: str
    table_name: str
    table_col: str
    data_df: pd.DataFrame = None

    def __post_init__(self):
        self.n_label = f"n_{self.name.lower().replace(' ', '_')}"
        self.pct_label = f"pct_{self.name.lower().replace(' ', '_')}"
