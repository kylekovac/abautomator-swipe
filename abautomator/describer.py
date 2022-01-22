from collections import defaultdict
from dataclasses import dataclass
from typing import List

from abautomator.metrics import BaseMetric

class InvalidColumns(Exception):
    pass

@dataclass
class Describer:
    metrics: List[BaseMetric]  # w/self.ser_metric_df populated by collector

    def __post_init__(self):
        self._check_metrics_for_col("exp_cond")
        self._check_metrics_for_col("echelon_user_id")
        self._check_metrics_for_col_prefix("n_")
        self._check_metrics_for_col_prefix("pct_")
    
    def _check_metrics_for_col(self, col_name):
        for metric in self.metrics:
            self._raise_error_if_metric_cols_missing(
                metric, col_name
            )

    def _raise_error_if_metric_cols_missing(self, metric, col_name):
        if col_name not in self._get_cols(metric.user_metric_df):
            raise InvalidColumns(f"{col_name} not present")
    
    def _get_cols(self, df):
        return list(self.metrics[0].user_metric_df)
    
    def _check_metrics_for_col_prefix(self, prefix):
        for metric in self.metrics:
            self._raise_error_if_metric_cols_missing_prefix(
                metric, prefix
            )
    
    def _raise_error_if_metric_cols_missing_prefix(self, metric, prefix):
        present = False
        for col in self._get_cols(metric.user_metric_df):
            if prefix in col:
                return True
        raise InvalidColumns(f"Prefix {prefix} not present")
    
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
