from dataclasses import dataclass

import pandas as pd


@dataclass
class Analyzer:
    """
    [ ] 1. Individual descriptions   -> Consolidated desc [exp_cond, metric, mean, est_est, count]
    [ ] 2. Consolidated descriptions -> Consolidated desc + confidence intervals
              - Useful for viz for all info to travel together at this point
    """
    outcomes: dict  # key is [metric name][cond name]
    ctrl_name: str
    base_df: pd.DataFrame=None

    def _get_ci(self):
        if self.base_desc is None:
            self._consolidate_descriptions()
        return self._add_basic_confidence_intervals()

    def _consolidate_descriptions(self):
        raw_data = []
        for metric in self.outcomes.keys():
            cond_dict = self.outcomes[metric]
            for exp_cond, desc_df in cond_dict.items():
                for n_or_pct_metric in list(desc_df.columns):
                    print(desc_df)
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
    
    def _add_basic_confidence_intervals(self):

        df = self.base_df.copy()

        df["upper_68_ci"] = df["mean"] + df["std"]
        df["lower_68_ci"] = df["mean"] - df["std"]

        df["upper_95_ci"] = df["mean"] + (2 * df["std"])
        df["lower_95_ci"] = df["mean"] - (2 * df["std"])

        return df

    def _add_abs_diff_confidence_intervals(self):

        df = self.base_df.copy()

        ctrl_df = self._get_ctrl_df(df)

        tx_df = df[df["exp_cond"] != self.ctrl_name]
        result_df = tx_df.merge(ctrl_df, how="left")
        print(result_df)
        # print(ctrl_df.head())
        # print(tx_df.head())

        # df["upper_68_ci"] = df["mean"] + df["std"]
        # df["lower_68_ci"] = df["mean"] - df["std"]

        # df["upper_95_ci"] = df["mean"] + (2 * df["std"])
        # df["lower_95_ci"] = df["mean"] - (2 * df["std"])

        return df
    
    def _get_ctrl_df(self, df):
        ctrl_df = df[df["exp_cond"] == self.ctrl_name]
        ctrl_df = self._rename_ctrl_cols(ctrl_df)
        ctrl_df = ctrl_df.drop(['exp_cond', 'factor_label'], axis=1)
        return ctrl_df
    
    def _rename_ctrl_cols(self, df):
        return df.rename(
            columns={
                "mean": "ctrl_mean",
                "std": "ctrl_std",
                "count": "ctrl_count",
            }
        )
