from dataclasses import dataclass, field
from datetime import date
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
