# Calculate sampling distributions
from dataclasses import dataclass
import math

import pandas as pd


def calc_sampling_distribution(user_metrics_df, exp):

  metrics = [col for col in user_metrics_df.columns if col not in ["echelon_user_id", "exp_cond"]]
  
  stat_df = user_metrics_df.groupby('exp_cond').agg(
    **_get_agg_params(metrics),
  )
  print(stat_df.head())
  stat_df.index = stat_df.index.str.replace(exp.name, "")

  data = []

  for tx_cond in exp.tx_conds:
    
    for metric in metrics:
      curr_row = {
        "exp_cond": tx_cond.name, "metric": metric, "metric_cond_label": (metric, tx_cond.name)
      }
      ctrl_desc = _get_sample_desc(stat_df, exp.ctrl_cond.name, metric)
      tx_desc = _get_sample_desc(stat_df, tx_cond.name, metric)

      curr_row["est_mean"] = _get_estimator_mean(tx_desc, ctrl_desc)
      curr_row["est_se"] = _get_estimator_standard_error(tx_desc, ctrl_desc)
    
      data.append(curr_row)
  
  return _convert_data_to_df(data)

def _convert_data_to_df(data):
  return pd.DataFrame(data)

def _get_estimator_mean(tx, ctrl):
  return tx.mean - ctrl.mean

def _get_estimator_standard_error(tx, ctrl):
  return math.sqrt(
    ( (tx.std * tx.std) / tx.size ) + \
    ( (ctrl.std * ctrl.std) / ctrl.size )
  )

def _get_agg_params(metrics):
  avg_params = {
    f"{metric}_mean": pd.NamedAgg(column=metric, aggfunc='mean') for metric in metrics
  }
  std_params = {
    f"{metric}_std": pd.NamedAgg(column=metric, aggfunc='std') for metric in metrics
  }
  n_params = {
    f"{metric}_size": pd.NamedAgg(column=metric, aggfunc='size') for metric in metrics
  }
  return _concat_dicts(avg_params, std_params, n_params)

def _concat_dicts(d1, d2, d3):
  result = dict(d1, **d2)
  result.update(d3)
  return result
  
def _get_sample_desc(stat_df: pd.DataFrame, cond_name: str, metric: str):
  return SampleMetricChars(
    cond_name,
    metric,
    stat_df[f"{metric}_mean"][cond_name],
    stat_df[f"{metric}_std"][cond_name],
    stat_df[f"{metric}_size"][cond_name],
  )

@dataclass
class SampleMetricChars:  # Characteristics
  cond: str
  metric: str
  mean: float
  std: float
  size: int

  def __repr__(self):
    return f"{self.cond} {self.metric} mean:{self.mean:.2f}±{self.std:.2f} size:{self.size}"
