import os
import pickle

import pandas as pd
import pytest
from sqlalchemy.sql import select

from abautomator import main
from tests import utils


def test_get_users_metrics_df(old_result, dfs):

    users_df, sessions_df, views_df = dfs

    assert len(users_df) > 10
    assert len(sessions_df) > 10

    result_df = main.get_user_metrics_df(users_df, [sessions_df, views_df])
    print(result_df.head())
    print(result_df.dtypes)

    assert len(result_df) > 10
    assert len(result_df) == len(users_df)
    assert len(result_df) == len(old_result)

@pytest.fixture
def dfs(conn, queries):
    users_query, sessions_query, views_query = queries

    users_df =  _df_from_cache("users", users_query, conn)
    sessions_df =  _df_from_cache("sessions", sessions_query, conn)
    views_df =  _df_from_cache("views", views_query, conn)

    return users_df, sessions_df, views_df

def _df_from_cache(name, query, conn):
    try:
        result = pickle.load(
            open(os.path.join("tests", f"{name}.p"), "rb" )
        )
    except FileNotFoundError:
        result =  main._get_query_df(query, conn)
        pickle.dump(
            result, open(os.path.join("tests", f"{name}.p"), "wb" )
        )
    return result

@pytest.fixture
def old_result(conn, sessions_query, users_query):
    return _get_old_result(conn, sessions_query, users_query)

def _get_old_result(conn, sessions_query, users_query):
    users_cte = users_query.cte("users")
    session_metric_cte = sessions_query.cte("sessions")
    user_metrics_query = select(
        users_cte.c.echelon_user_id,
        users_cte.c.exp_cond,
        session_metric_cte.c.n_user_sessions,
        ).select_from(
            users_cte.join(session_metric_cte, users_cte.c.echelon_user_id == session_metric_cte.c.echelon_user_id, isouter=True)
    )
    return _df_from_cache("old", user_metrics_query, conn)

def test_sampling_distribution(dfs, exp):

    users_df, sessions_df, views_df = dfs

    result_df = main.get_user_metrics_df(users_df, [sessions_df, views_df])

    pd.set_option('display.max_columns', None)

    result_df = main.calc_sampling_distribution(result_df, exp)

    print(result_df.head(10))

    pickle.dump(
        result_df, open(os.path.join("tests", f"sampling_dist.p"), "wb" )
    )
