from dataclasses import dataclass, field
from datetime import date
from typing import List

import pandas as pd

from abautomator import metric

class InvalidName(Exception):
  pass


@dataclass
class Outcome:
  """ Outcome of metric as result of condition """
  metric: str
  cond: str
  desc: pd.DataFrame


@dataclass
class Condition:
  raw_name: str
  name: str = None
  outcomes: List[Outcome] = None

  def set_name(self, exp_name):
    self.name = self.raw_name.replace(exp_name, "")


@dataclass
class Experiment:
  ctrl_cond: Condition       # names are col values
  tx_conds: List[Condition]  # names are col values
  metrics: List[metric.Metric]
  event: str                 # table/thing user does to become exp participant
  event_prop: str            # table col
  start_dt: date
  end_dt: date=None
  devices: List[str]=field(default_factory=lambda: ['android', 'ios'])

  def __post_init__(self):
    self.name = self._get_name(
      self.ctrl_cond.raw_name, self.tx_conds[0].raw_name
    )
    self._clean_up_cond_labels()
  
  def _clean_up_cond_labels(self):
    self.ctrl_cond.set_name(self.name)
    for tx in self.tx_conds:
      tx.set_name(self.name)
  
  def _get_name(self, ctrl: str, tx: str):
    end = 0
    for i, j in zip(ctrl, tx):
      if i != j:
        return ctrl[:end]
      end += 1
    
    raise InvalidName("Experiment or Condition Name is invalid")

  def get_outcomes(self):
    pass

  def get_queryable_conds(self):
    conds = [self.ctrl_cond] + self.tx_conds
    return [f"{self.name}{cond.name}" for cond in conds]

