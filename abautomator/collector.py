""" Collects experiment data from BigQuery"""
from datetime import date
from dataclasses import dataclass, field
from typing import List

import pandas as pd
import sqlalchemy

from abautomator import get_query, get_df


@dataclass
class Metric:
    name: str
    table_name: str
    table_col: str
    data_df: pd.DataFrame = None

    def __post_init__(self):
        self.n_label = f"n_{self.name.lower().replace(' ', '_')}"
        self.pct_label = f"pct_{self.name.lower().replace(' ', '_')}"


@dataclass
class Collector:
    engine: sqlalchemy.engine.Engine 
    conds: List[str]                  # column values
    metrics: List[Metric]             # metadata for getting metric data
    event: str                        # table/thing user does to become exp participant
    event_prop: str                   # table col
    start_dt: date
    end_dt: date=None
    devices: List[str]=field(default_factory=lambda: ['android', 'ios'])

    def collect_data(self):
        with self.engine.connect() as conn:
            self._populate_data_dfs(conn)

    def _populate_data_dfs(self, conn):
        for metric in self.metrics:
            metric.data_df = get_df.get_df_from_query(
                get_query.get_metric_query(self.engine, self, metric),
                conn,
            )
