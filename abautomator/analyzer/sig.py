""" Statisical significance functionality of the analyzer """
import numpy as np
import scipy.stats
import logging

from abautomator.analyzer import utils

LOGGER = logging.getLogger()

def get_pvalue_for_pop_mean_or_proportion(row):

    if utils._confirm_stats_not_calculable(row):
        return np.nan

    if row["metric"].startswith("n_"):
        return _get_pvalue_for_pop_mean(row)
    return _get_pvalue_for_pop_proportion(row)
    
def _get_pvalue_for_pop_mean(row):
    if 0.5 <= (row["ctrl_std"] / row ["tx_std"]) <= 2:
        return _get_pvalue_for_pop_mean_w_equal_variance(row)
    return _get_pvalue_for_pop_mean_w_unequal_variance(row)

def _get_pvalue_for_pop_mean_w_equal_variance(row):
    return _get_pvalue_for_pop_mean_given_df(
        row, df=row["tx_count"] + row["ctrl_count"] - 2
    )

def _get_pvalue_for_pop_mean_given_df(row, df):
    t_score = row["mean"]/row["std"]  # AKA test statistic
    # t_crit = scipy.stats.t.ppf(q=1-.05/2, df=df)
    return scipy.stats.t.sf(np.abs(t_score), df) * 2  # two-sided pvalue = Prob(abs(t)>tt)
 

def _get_pvalue_for_pop_mean_w_unequal_variance(row):
    return _get_pvalue_for_pop_mean_given_df(
        row, df=min(row["tx_count"] - 1, row["ctrl_count"] - 1)
    )

def _get_pvalue_for_pop_proportion(row):
    z_score = row["mean"]/row["std"]  # AKA test statistic
    # z_crit = scipy.stats.norm.ppf(q=1-.05/2, df=df)
    return scipy.stats.norm.sf(abs(z_score))