from dataclasses import dataclass, field
from datetime import date
from typing import List

class InvalidName(Exception):
  pass

@dataclass
class Experiment:
  ctrl_cond: str           # col values
  tx_conds: List[str]      # col values
  event: str               # table
  event_prop: str          # table col
  start_dt: date
  end_dt: date=None
  devices: List[str]=field(default_factory=lambda: ['android', 'ios'])

  def __post_init__(self):
    self.name = self._get_name(self.ctrl_cond, self.tx_conds[0])
    self._clean_up_cond_labels()
  
  def _clean_up_cond_labels(self):
    self.ctrl_cond = self.ctrl_cond.replace(self.name, "")
    new_txs = []
    for tx in self.tx_conds:
      new_txs.append(tx.replace(self.name, ""))
    self.tx_conds = new_txs
  
  def _get_name(self, ctrl: str, tx: str):
    end = 0
    for i, j in zip(ctrl, tx):
      if i != j:
        return ctrl[:end]
      end += 1
    
    raise InvalidName("Experiment or Condition Name is invalid")    

  def get_queryable_conds(self):
    conds = [self.ctrl_cond] + self.tx_conds
    return [f"{self.name}{cond}" for cond in conds]
