from sqlalchemy.sql import selectable

from abautomator.metrics.metric_lookup import METRIC_LOOKUP

def test_metrics_build_queries(coll):

    for _, metric in METRIC_LOOKUP.items():
        query = metric._get_metric_query(coll)
        assert isinstance(query, selectable.Select)


def test_get_metric_df(coll, conn, name):
    # name is passed in via the pytest cli --name flag

    metric = METRIC_LOOKUP[name]
    metric_df = metric._get_metric_df(coll, conn)
    col_names = list(metric_df.columns)
    
    assert len(metric_df) > 10
    assert metric.n_label in col_names
    assert metric.pct_label in col_names
