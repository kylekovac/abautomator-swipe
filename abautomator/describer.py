from collections import defaultdict
from dataclasses import dataclass
from typing import List

from abautomator.metrics import BaseMetric

class InvalidColumns(Exception):
    pass

@dataclass
class Describer:
    metrics: List[BaseMetric]

    def __post_init__(self):
        self._raise_error_if_columns_dont_contain("exp_cond")
        self._raise_error_if_columns_dont_contain("n_user_sessions")
    
    def _raise_error_if_columns_dont_contain(self, col_name):
        cols_to_check = list(self.metrics[0].user_metric_df)
        if col_name not in cols_to_check:
            raise InvalidColumns(f"{col_name} not in {cols_to_check}")
    
    def describe_data(self, exp_name):
        self._clean_data_dfs(exp_name)
        return self._generate_outcome_desc()
    
    def _clean_data_dfs(self, exp_name):
        for metric in self.metrics:
            self._remove_exp_name_from_exp_cond(exp_name, metric.user_metric_df)
    
    def _remove_exp_name_from_exp_cond(self, exp_name, user_metric_df):
        user_metric_df["exp_cond"] = user_metric_df["exp_cond"].str.replace(
            exp_name, ""
        )
    
    def _generate_outcome_desc(self):
        outcomes = defaultdict(lambda: dict())  # keyed to [metric][cond]

        for metric in self.metrics:
            df = metric.user_metric_df
            conds = df["exp_cond"].unique()
            for cond in conds:
                outcomes[metric.name][cond] = df[df["exp_cond"] == cond].describe()
        return outcomes
