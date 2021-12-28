
def test_collect_data(coll_single_metric):
    coll_single_metric.metrics
    coll_single_metric.collect_data()
    print(coll_single_metric.metrics[0].data_df.head())

    assert len(coll_single_metric.metrics[0].data_df) > 10
