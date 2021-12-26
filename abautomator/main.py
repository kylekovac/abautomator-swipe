from dataclasses import dataclass
import math

import pandas as pd
from sqlalchemy import case
from sqlalchemy.engine import *
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from abautomator.experiment import Experiment


def get_users_query(engine: Engine, exp: Experiment):
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

  def __post_init__(self):
    self.n_label = f"n_{self.name.lower().replace(' ', '_')}"
    self.pct_label = f"pct_{self.name.lower().replace(' ', '_')}"

  # def n_label(self):
  #   return f"n_{self.name.lower().replace(' ', '_')}"

  # def pct_label(self):
  #   return f"pct_{self.name.lower().replace(' ', '_')}"

def get_metric_query(engine: Engine, exp: Experiment, metric: Metric):
  table = Table(f'echelon.{metric.table_name}', MetaData(bind=engine), autoload=True)

  result = select(
      table.c.echelon_user_id,
      func.count(getattr(table.c, metric.table_col)).label(metric.n_label),
      case(
        (
          func.count(getattr(table.c, metric.table_col)) > 0, 1
        ),
        else_=0
      ).label(metric.pct_label),
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
  
  result = _fill_nan_metrics_with_zeros(result)

  return result

def _fill_nan_metrics_with_zeros(df):
  for col in df.columns:
    if col not in ["echelon_user_id", "exp_cond"]:
      df[col] = df[col].fillna(0)
  return df

def calc_sampling_distribution(user_metrics_df, exp):

  metrics = [col for col in user_metrics_df.columns if col not in ["echelon_user_id", "exp_cond"]]
  
  stat_df = user_metrics_df.groupby('exp_cond').agg(
    **_get_agg_params(metrics),
  )

  result = []  

  for tx_cond in exp.tx_conds:

    curr_row = {"exp_cond": tx_cond}
    
    for metric in metrics:
      ctrl_chars = _get_sample_chars(stat_df, exp.ctrl_cond, metric)      
      tx_chars = _get_sample_chars(stat_df, tx_cond, metric)

      curr_row[f"{metric}_est"] = _get_estimator(tx_chars, ctrl_chars)
      curr_row[f"{metric}_ci"] = _get_estimator_ci(tx_chars, ctrl_chars) # confidence interval
    
    result.append(curr_row)

  return pd.DataFrame(result).set_index("exp_cond")

def _get_estimator(tx, ctrl):
  return tx.mean - ctrl.mean

def _get_estimator_ci(tx, ctrl):
  return 1.96 * _get_estimator_standard_error(tx, ctrl)

def _get_estimator_standard_error(tx, ctrl):
  return math.sqrt(
    ( (tx.var * tx.var) / tx.size ) + \
    ( (ctrl.var * ctrl.var) / ctrl.size )
  )

def _get_agg_params(metrics):
  avg_params = {
    f"{metric}_mean": pd.NamedAgg(column=metric, aggfunc='mean') for metric in metrics
  }
  var_params = {
    f"{metric}_var": pd.NamedAgg(column=metric, aggfunc='var') for metric in metrics
  }
  n_params = {
    f"{metric}_size": pd.NamedAgg(column=metric, aggfunc='size') for metric in metrics
  }
  return _concat_dicts(avg_params, var_params, n_params)

def _concat_dicts(d1, d2, d3):
  result = dict(d1, **d2)
  result.update(d3)
  return result
  
def _get_sample_chars(stat_df, condition, metric):
  return SampleMetricChars(
    condition,
    metric,
    stat_df[f"{metric}_mean"][condition],
    stat_df[f"{metric}_var"][condition],
    stat_df[f"{metric}_size"][condition],
  )

@dataclass
class SampleMetricChars:  # Characteristics
  cond: str
  metric: str
  mean: float
  var: float
  size: int

  def __repr__(self):
    return f"{self.cond} {self.metric} mean:{self.mean:.2f}±{self.var:.2f} size:{self.size}"
