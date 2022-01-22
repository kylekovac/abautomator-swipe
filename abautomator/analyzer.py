from dataclasses import dataclass
import numpy as np

import pandas as pd
from pandas.core.frame import DataFrame


@dataclass
class Analyzer:
    outcomes: dict  # key is [metric name][cond name]
    ctrl_name: str
    base_df: pd.DataFrame=None

    def get_basic_confidence_intervals(self) -> pd.DataFrame:

        df = self.base_df.copy()
        df = self._calculate_confidence_interval(df)

        return df
    
    def _calculate_confidence_interval(self, df):
        # Precondition: df has "mean" and "std" columns
        df["upper_68_ci"] = df["mean"] + df["std"]
        df["lower_68_ci"] = df["mean"] - df["std"]

        df["upper_95_ci"] = df["mean"] + (2 * df["std"])
        df["lower_95_ci"] = df["mean"] - (2 * df["std"])

        return df

    def consolidate_descriptions(self):
        raw_data = []
        for metric in self.outcomes.keys():
            cond_dict = self.outcomes[metric]
            for exp_cond, desc_df in cond_dict.items():
                for n_or_pct_metric in list(desc_df.columns):
                    curr_row = {
                        "exp_cond": exp_cond,
                        "metric": n_or_pct_metric,
                        "mean": desc_df[n_or_pct_metric]["mean"],
                        "std": desc_df[n_or_pct_metric]["std"],
                        "count": desc_df[n_or_pct_metric]["count"],
                        "factor_label": (n_or_pct_metric, exp_cond),
                    }
                    raw_data.append(curr_row)

        self.base_df = pd.DataFrame(raw_data)

    
    def get_rel_diff_confidence_intervals(self) -> pd.DataFrame:

        df = self.get_abs_diff_confidence_intervals()
        df = df.rename(columns={"mean": "abs_mean", "std": "abs_std"})
        df["mean"] =(( df["abs_mean"] / df["ctrl_mean"] ) * 100)
        df["std"] = df["abs_std"] / df["ctrl_mean"] * 100

        return self._calculate_confidence_interval(df)


    def get_abs_diff_confidence_intervals(self) -> pd.DataFrame:

        df = self._get_abs_diff_desc()
        return self._calculate_confidence_interval(df)
    
    def _get_abs_diff_desc(self):

        df = self.base_df.copy()

        ctrl_df = self._get_ctrl_df(df)
        tx_df = self._get_tx_df(df)

        result_df = tx_df.merge(ctrl_df, how="left")
        result_df = self._add_diff_desc(result_df)

        return result_df
    
    def _add_diff_desc(self, df):
        df["mean"] = df["tx_mean"] - df["ctrl_mean"]
        df = self._add_diff_std(df)
        return df
    
    def _add_diff_std(self, df):

        df["std"] = np.sqrt(
            ( df["tx_std"]**2 / df["tx_count"] ) \
            + ( df["ctrl_std"]**2 / df["ctrl_count"] )
            )

        return df
    
    def _get_ctrl_df(self, df):
        ctrl_df = df[df["exp_cond"] == self.ctrl_name]
        ctrl_df = self._rename_ctrl_cols(ctrl_df)
        ctrl_df = ctrl_df.drop(['exp_cond', 'factor_label'], axis=1)
        return ctrl_df
    
    def _rename_ctrl_cols(self, df):
        return self._rename_cols(df, "ctrl")
    
    def _rename_cols(self, df, prefix):
        return df.rename(
            columns={
                "mean": f"{prefix}_mean",
                "std": f"{prefix}_std",
                "count": f"{prefix}_count",
            }
        )

    def _get_tx_df(self, df):
        tx_df = df[df["exp_cond"] != self.ctrl_name]
        tx_df = self._rename_tx_cols(tx_df)
        return tx_df
    
    def _rename_tx_cols(self, df):
        return self._rename_cols(df, "tx")
