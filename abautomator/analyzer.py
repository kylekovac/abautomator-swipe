from dataclasses import dataclass

import pandas as pd


@dataclass
class Analyzer:
    """
    [ ] 1. Individual descriptions   -> Consolidated desc [exp_cond, metric, est_mean, est_est, count]
    [ ] 2. Consolidated descriptions -> Consolidated desc + confidence intervals
              - Useful for viz for all info to travel together at this point
    """
    outcomes: dict  # key is [metric name][cond name]
    ctrl_name: str

    def analze(self):
        pass

    def _consolidate_descriptions(self):
        raw_data = []
        for metric in self.outcomes.keys():
            cond_dict = self.outcomes[metric]
            for exp_cond, desc_df in cond_dict.items():
                for n_or_pct_metric in list(desc_df.columns):
                    curr_row = {
                        "exp_cond": exp_cond,
                        "metric": n_or_pct_metric,
                        "est_mean": desc_df[n_or_pct_metric]["mean"],
                        "est_std": desc_df[n_or_pct_metric]["std"],
                        "est_count": desc_df[n_or_pct_metric]["count"],
                    }
                    raw_data.append(curr_row)
        
        return pd.DataFrame(raw_data)
    
    def _add_confidence_intervals():
        pass
