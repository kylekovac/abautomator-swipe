from datetime import date
from dataclasses import dataclass, field

from google.cloud import bigquery
import sqlalchemy
from sqlalchemy.engine import *
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

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
      getattr(table.c, exp.event_prop).label("cohort"),
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
  table_name: str
  table_col: str

def get_metric_query(engine, exp, metric):
  table = Table(f'echelon.{metric.table_name}', MetaData(bind=engine), autoload=True)

  result = select(
      table.c.echelon_user_id,
      func.count(getattr(table.c, metric.table_col)).label("n_events")
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

def get_user_metrics_df(users_df, metric_df):
  return users_df.join(metric_df, on="echelon_user_id", how="left")