""" Statisical functionality of the analyzer """
import numpy as np
import logging

LOGGER = logging.getLogger()

def get_std_for_pop_mean_or_proportion(row):
    # https://stats.libretexts.org/Bookshelves/Applied_Statistics/Book%3A_Business_Statistics_(OpenStax)/10%3A_Hypothesis_Testing_with_Two_Samples/10.04%3A_Comparing_Two_Independent_Population_Proportions
    if row["metric"].startswith("n_"):
        return _get_std_for_pop_mean(row)
    return _get_std_for_pop_proportion(row)
    
def _get_std_for_pop_mean(row):
    # https://online.stat.psu.edu/stat500/book/export/html/576#:~:text=As%20with%20comparing%20two%20population,is%20%CE%BC%201%20%E2%88%92%20%CE%BC%202%20.
    if 0.5 <= (row["ctrl_std"] / row ["tx_std"]) <= 2:
        return _get_std_for_pop_mean_w_equal_variance(row)
    return _get_std_for_pop_mean_w_unequal_variance(row)

def _get_std_for_pop_mean_w_equal_variance(row):
    pooled_std = np.sqrt(
        (
            (row["ctrl_count"] - 1) * (row["ctrl_std"] ** 2) + (row["tx_count"] - 1) * (row["tx_std"] ** 2)
        ) / (row["ctrl_count"] + row["tx_count"] - 2)
    )
    sqrt_inverse = np.sqrt(
        (1 / row["ctrl_count"]) + (1 / row["tx_count"])
    )
    return pooled_std * sqrt_inverse    

def _get_std_for_pop_mean_w_unequal_variance(row):
    return np.sqrt(
        ( row["tx_std"]**2 / row["tx_count"] ) \
        + ( row["ctrl_std"]**2 / row["ctrl_count"] )
    )

def _get_std_for_pop_proportion(row):
    _check_sample_size(row)

    ctrl_succ = row["ctrl_mean"] * row["ctrl_count"]
    tx_succ = row["tx_mean"] * row["tx_count"]
    pooled_succ = ctrl_succ + tx_succ
    pooled_count = row["ctrl_count"] + row["tx_count"]
    pooled_prop = pooled_succ / pooled_count
    
    return np.sqrt(
        ( pooled_prop * (1 - pooled_prop)) / pooled_count
    )

def _check_sample_size(row):
    if row["ctrl_count"] < 30 or row["tx_count"] < 30:
        LOGGER.warning("STD Calc Assumption violation! N < 30 for a tx")
