import pytest

from sqlalchemy.sql import select


from tests import utils

def test_add_exp_cond_to_metric(sessions_metric, users_df, sessions_df):
    result_df = sessions_metric._add_exp_cond_to_metric(users_df, sessions_df)

    assert len(result_df) > 10
    assert len(result_df.columns) > len(users_df.columns)
    assert len(result_df.columns) > len(sessions_df.columns)

def test_populate_user_metric_df(sessions_metric, coll_w_users_df, conn):
    sessions_metric.populate_user_metric_df(coll_w_users_df, conn)

    result_df = sessions_metric.user_metric_df
    assert len(result_df) > 10
    assert len(result_df.columns) > len(coll_w_users_df.users_df.columns)
    assert "exp_cond" in list(result_df.columns)
    assert "n_user_sessions" in list(result_df.columns)


def test_populate_user_metric_df_counts(sessions_metric, dfs,  old_result):
    users_df, sessions_df, = dfs

    assert len(users_df) > 10
    assert len(sessions_df) > 10

    result_df = sessions_metric._add_exp_cond_to_metric(users_df, sessions_df)

    assert len(result_df) > 10
    assert len(old_result) > 10
    assert len(result_df) == len(users_df)
    assert len(result_df) == len(old_result)


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
    return utils.df_from_cache("old", user_metrics_query, conn)
