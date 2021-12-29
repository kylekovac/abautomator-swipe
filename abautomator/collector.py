""" Collects experiment data from BigQuery"""
from datetime import date
from dataclasses import dataclass, field
from typing import List

import pandas as pd
import sqlalchemy
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select
from sqlalchemy.sql.selectable import Selectable

from abautomator import get_query, get_df, metric


@dataclass
class Collector:
    engine: sqlalchemy.engine.Engine
    conds: List[str]                  # column values
    metrics: List[metric.Metric]             # metadata for getting metric data
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
            self.users_df = get_df.get_df_from_query(
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

        result = add_time_frame(result, table, self.start_dt, self.end_dt)
        return result
    
    def _populate_metric_data_dfs(self, conn):
        for metric in self.metrics:
            metric_df = get_df.get_df_from_query(
                self._get_metric_query(metric), conn,
            )
            metric.data_df = self._add_exp_cond_to_metric(metric_df)
    
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
        result = add_time_frame(result, table, self.start_dt, self.end_dt)

        return result

    def _add_exp_cond_to_metric(self, metric_df):
        return get_df.get_user_metrics_df(self.users_df, metric_df)

def add_time_frame(query: Selectable, table: Table, start_dt: date = None, end_dt: date = None):
  if start_dt:
    query = query.where(
      table.c.event_date >= start_dt
    )
  if end_dt:
    query = query.where(
      table.c.event_date <= end_dt
    )
  return query






