

def _confirm_stats_not_calculable(row):
    return row["ctrl_count"] == 0 \
        or row["tx_count"] == 0   \
        or row["tx_std"] == 0     \
        or (row["ctrl_count"] + row["tx_count"] == 1)