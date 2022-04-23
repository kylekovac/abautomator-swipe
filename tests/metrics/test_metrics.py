""" Test that individual metrics run as expected

 - name is passed in via the pytest cli --name flag
 - to run all test run --name all
 - no test are run without --name flag
"""
from sqlalchemy.sql import selectable

from abautomator import config
from abautomator.metrics import METRIC_LOOKUP
from abautomator.utils import get_df_from_query
from tests import utils
from tests.metrics.raw_queries import RAW_QUERIES


def test_metrics_build_queries(coll, name):

    for metric in _get_metrics_to_test(name):
        query = metric._get_metric_query(coll.engine, coll.dt_range)
        assert isinstance(query, selectable.Select)


def _get_metrics_to_test(name):
    if name == "all":
        result = METRIC_LOOKUP.values()
    elif name == "default name":
        result = []
    else:
        result = [METRIC_LOOKUP[name]]

    return result


def test_get_metric_df(coll, conn, name):

    for metric in _get_metrics_to_test(name):
        metric_df = metric._get_metric_df(coll.engine, conn, coll.dt_range)
        utils.cache_obj(metric_df, name)  # speed up test_get_user_metric_df
        old_df = _get_metric_df_from_old_query(metric, conn, coll.dt_range.start)
        col_names = list(metric_df.columns)
        
        assert len(metric_df) > 10
        assert len(metric_df) == len(old_df)

        print(f"obj len {len(metric_df)}")
        print(f"old len {len(old_df)}")

        _assert_items_in_list(
            items=["echelon_user_id", metric.n_label, metric.pct_label],
            list_=col_names,
        )

def _get_metric_df_from_old_query(metric, conn, start_dt):
    query = RAW_QUERIES[metric.name].format(
        dataset=config.GCP_DATASET,
        start_dt=start_dt,
    )
    print(query)
    old_df = utils.df_from_cache(
        f"{metric.name}_old_query", query, conn
    )
    return old_df

def _assert_items_in_list(items, list_):
    for item in items:
        assert item in list_

def test_get_user_metric_df(coll_w_users_df, conn, name):

    for metric in _get_metrics_to_test(name):
        query = metric._get_metric_query(coll_w_users_df.engine, coll_w_users_df.dt_range)
        metric_df = utils.df_from_cache(metric.name, query, conn)

        user_metric_df = metric._add_exp_cond_to_metric(
            coll_w_users_df.users_df, metric_df
        )

        assert len(user_metric_df) > 10
        assert len(user_metric_df) == len(coll_w_users_df.users_df)
        assert len(user_metric_df.columns) > len(coll_w_users_df.users_df.columns)
        assert len(user_metric_df.columns) > len(metric_df.columns)
        _assert_items_in_list(
            items=["echelon_user_id", "exp_cond", metric.n_label, metric.pct_label],
            list_=list(user_metric_df.columns),
        )

        # print(user_metric_df.head())

        
