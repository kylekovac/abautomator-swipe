# Calculate sampling distributions
from dataclasses import dataclass
import math

import pandas as pd


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
