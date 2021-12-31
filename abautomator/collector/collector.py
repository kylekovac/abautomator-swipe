""" Collects experiment data from BigQuery"""
from datetime import date
from dataclasses import dataclass, field
from typing import List

import sqlalchemy
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from abautomator import metric, utils


@dataclass
class Collector:
    engine: sqlalchemy.engine.Engine
    conds: List[str]                  # column values
    metrics: List[metric.Metric]      # Metric data/metadata
    event: str                        # table/thing user does to become exp participant
    event_prop: str                   # table col with exp_cond info
    start_dt: date
    end_dt: date=None
    users_df = None
    devices: List[str]=field(default_factory=lambda: ['android', 'ios'])

    def collect_data(self):
        with self.engine.connect() as conn:
            self._populate_users_df(conn)
            self._populate_metric_data_dfs(conn)
    
    def _populate_users_df(self, conn):
        if self.users_df is None:
            self.users_df = utils.get_df_from_query(
                self._get_users_query(), conn,
            )

    def _get_users_query(self):
        table = Table(f'echelon.{self.event}', MetaData(bind=self.engine), autoload=True)

        result = select(
            table.c.echelon_user_id,
            getattr(table.c, self.event_prop).label("exp_cond"),
        ).where(
            getattr(table.c, self.event_prop).in_(self.conds)
        ).group_by(
            table.c.echelon_user_id, 
            getattr(table.c, self.event_prop),
        )
        # Ommitting first_event_datetime for now

        result = utils.add_time_frame(result, table, self.start_dt, self.end_dt)
        return result
    
    def _get_metric_query(self, metric: metric.Metric):
        table = Table(f'echelon.{metric.table_name}', MetaData(bind=self.engine), autoload=True)

        result = select(
            table.c.echelon_user_id,
            func.count(getattr(table.c, metric.table_col)).label(metric.n_label),
            sqlalchemy.case(
                (
                func.count(getattr(table.c, metric.table_col)) > 0, 1
                ),
                else_=0
            ).label(metric.pct_label),
        ).group_by(
            table.c.echelon_user_id,
        )
        result = utils.add_time_frame(result, table, self.start_dt, self.end_dt)

        return result
    
    def _populate_metric_data_dfs(self, conn):
        for metric in self.metrics:
            # metric.populate_data_df(self)  # Ideal state
            metric_df = utils.get_df_from_query(
                self._get_metric_query(metric), conn,
            )
            metric.data_df = self._add_exp_cond_to_metric(metric_df)
    
    def _add_exp_cond_to_metric(self, metric_df):
        return self.get_user_metrics_df(metric_df)

    def get_user_metrics_df(self, metric_df):
        result = self.users_df.copy()
        result = result.merge(metric_df, on="echelon_user_id", how="left")
    
        result = _fill_nan_metrics_with_zeros(result)

        return result

def _fill_nan_metrics_with_zeros(df):
  for col in df.columns:
    if col not in ["echelon_user_id", "exp_cond"]:
      df[col] = df[col].fillna(0)
  return df








