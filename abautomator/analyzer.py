from dataclasses import dataclass
import numpy as np

import pandas as pd
from pandas.core.frame import DataFrame


@dataclass
class Analyzer:
    outcomes: dict  # key is [metric name][cond name]
    ctrl_name: str
    base_df: pd.DataFrame=None

    def __post_init__(self):
        self._consolidate_descriptions()

    def _consolidate_descriptions(self):
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
                    }
                    raw_data.append(curr_row)

        self.base_df = pd.DataFrame(raw_data)

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

        pop_mean_df = df[df['metric'].str.startswith("n_")].copy()
        pop_prop_df = df[df['metric'].str.startswith("pct_")].copy()

        pop_mean_df = self._add_std_for_pop_mean(pop_mean_df)
        pop_prop_df = self._add_std_for_pop_proportion(pop_prop_df)

        return pd.concat([pop_mean_df, pop_prop_df])

    
    def _add_std_for_pop_mean(self, df):
        # https://online.stat.psu.edu/stat500/book/export/html/576#:~:text=As%20with%20comparing%20two%20population,is%20%CE%BC%201%20%E2%88%92%20%CE%BC%202%20.

        df["std"] = np.sqrt(
            ( df["tx_std"]**2 / df["tx_count"] ) \
            + ( df["ctrl_std"]**2 / df["ctrl_count"] )
        )

        return df
    
    def _add_std_for_pop_proportion(self, df):
        # https://stats.libretexts.org/Bookshelves/Applied_Statistics/Book%3A_Business_Statistics_(OpenStax)/10%3A_Hypothesis_Testing_with_Two_Samples/10.04%3A_Comparing_Two_Independent_Population_Proportions
        
        df["ctrl_succ"] = df["ctrl_mean"] * df["ctrl_count"]
        df["tx_succ"] = df["tx_mean"] * df["tx_count"]
        df["pooled_succ"] = df["ctrl_succ"] + df["tx_succ"]
        df["pooled_count"] = df["ctrl_count"] + df["tx_count"]
        df["pooled_prop"] = df["pooled_succ"] / df["pooled_count"]

        df["std"] = np.sqrt(
            ( df["pooled_prop"] * (1 - df["pooled_prop"]) ) \
            / df["pooled_count"] \
        )

        df = df.drop(
            ['ctrl_succ', "tx_succ", "pooled_succ", "pooled_count", "pooled_prop"],
            axis=1,
        )

        return df
    
    def _get_ctrl_df(self, df):
        ctrl_df = df[df["exp_cond"] == self.ctrl_name]
        ctrl_df = self._add_prefix_to_stat_cols(ctrl_df, "ctrl")
        ctrl_df = ctrl_df.drop(['exp_cond'], axis=1)
        return ctrl_df
    
    def _add_prefix_to_stat_cols(self, df, prefix):
        return df.rename(
            columns={
                "mean": f"{prefix}_mean",
                "std": f"{prefix}_std",
                "count": f"{prefix}_count",
            }
        )

    def _get_tx_df(self, df):
        tx_df = df[df["exp_cond"] != self.ctrl_name]
        tx_df = self._add_prefix_to_stat_cols(tx_df, "tx")
        return tx_df
