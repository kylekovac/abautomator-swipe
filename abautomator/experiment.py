from datetime import date
from dataclasses import dataclass
from typing import List

from sqlalchemy import create_engine

from abautomator import config, collector, describer, utils, metrics, analyzer
from abautomator.metrics import metric_lookup

class InvalidName(Exception):
  pass



@dataclass
class Experiment:
    ctrl_name: str
    tx_names: List[str]
    metrics: List[metrics.BaseMetric]
    start_dt: date
    end_dt: date=None
    exp_name: str=None

    def __post_init__(self):
        self.name = self._get_name(
            self.ctrl_name, self.tx_names[0],
        )
    
    def _get_name(self, ctrl: str, tx: str):
        end = 0
        for i, j in zip(ctrl, tx):
            if i != j:
                return ctrl[:end]
            end += 1
        
        raise InvalidName("Experiment or Condition Name is invalid")    

    def run_experiment(self):

        coll = self.get_collector()
        coll.collect_data()

        # init and run the describer
        desc = describer.Describer(
            metrics=coll.metrics
        )
        outcomes_dict = desc.describe_data(self.exp_name)

        analy = analyzer.Analyzer(
            outcomes=outcomes_dict,
            ctrl_name=self.ctrl_name,
        )

        # init and run the analyzer

        # dump data into a cache (?) not neccisarily here

    def get_collector(self):
        return collector.Collector(
            engine=create_engine(f'bigquery://{config.GCP_PROJECT_ID}'),
            conds=self._get_conds(),
            metrics=get_metrics(),
            event="segment_signup_flow_started",
            event_prop="context_traits_onboarding_flow_001",
            start_dt=utils.get_yesterday(),
        )

    def _get_conds(self) -> List[str]:
        return [self.ctrl_name] + self.tx_names

def get_metrics():
    return [
        metric_lookup.METRIC_LOOKUP["granted_location"],
        metric_lookup.METRIC_LOOKUP["granted_notifs"],
    ]

# def get_analyzer():