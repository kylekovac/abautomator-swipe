from datetime import date
from dataclasses import dataclass, field


import pandas as pd
import numpy as np
from sqlalchemy import case
from sqlalchemy.engine import *
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from google.cloud import bigquery

from abautomator.config import GCP_PROJECT_ID


from typing import List


@dataclass
class Experiment:
  ctrl_cond: str           # col values
  tx_conds: List[str]      # col values
  event: str               # table
  event_prop: str          # table col
  start_dt: date
  end_dt: date=None
  devices: List[str]=field(default_factory=lambda: ['android', 'ios'])

  def all_conds(self):
    return [self.ctrl_cond] + self.tx_conds


def get_users_query(engine, exp):
  table = Table(f'echelon.{exp.event}', MetaData(bind=engine), autoload=True)

  result = select(
      table.c.echelon_user_id,
      getattr(table.c, exp.event_prop).label("exp_cond"),
  ).where(
      getattr(table.c, exp.event_prop).in_(exp.all_conds())
  ).group_by(
      table.c.echelon_user_id, 
      getattr(table.c, exp.event_prop),
  )
  # Ommitting first_event_datetime for now

  result = add_time_frame(result, table, exp.start_dt, exp.end_dt)
  return result

@dataclass
class Metric:
  name: str
  table_name: str
  table_col: str

  def n_label(self):
    return f"n_{self.name.lower().replace(' ', '_')}"

  def pct_label(self):
    return f"pct_{self.name.lower().replace(' ', '_')}"

def get_metric_query(engine, exp, metric):
  table = Table(f'echelon.{metric.table_name}', MetaData(bind=engine), autoload=True)

  result = select(
      table.c.echelon_user_id,
      func.count(getattr(table.c, metric.table_col)).label(metric.n_label()),
      case(
        (
          func.count(getattr(table.c, metric.table_col)) > 0, 1
        ),
        else_=0
      ).label(metric.pct_label()),
  ).group_by(
      table.c.echelon_user_id,
  )
  result = add_time_frame(result, table, exp.start_dt, exp.end_dt)

  return result

def add_time_frame(query, table, start_dt=None, end_dt=None):
  if start_dt:
    query = query.where(
      table.c.event_date >= start_dt
    )
  if end_dt:
    query = query.where(
      table.c.event_date <= end_dt
    )
  return query

def _get_query_df(query, conn):
  result = pd.read_sql(query, conn)
  result['echelon_user_id'] = result['echelon_user_id'].astype("string")
  return result

def get_user_metrics_df(users_df, metrics):
  result = users_df
  for metric_df in metrics:
    result = result.merge(metric_df, on="echelon_user_id", how="left")
  return result

def calc_sampling_distribution(user_metrics_df):
  result = user_metrics_df.groupby(["exp_cond"], as_index=False).mean()
  return result