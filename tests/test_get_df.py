import pytest
from sqlalchemy.sql import select

from abautomator import get_df
from tests import utils


def test_get_df_from_query(users_query, conn):
    result = get_df.get_df_from_query(users_query, conn)
    assert len(result) > 10

def test_get_users_metrics_df(dfs):
    users_df, sessions_df, = dfs
    result_df = get_df.get_user_metrics_df(users_df, sessions_df)
    assert len(result_df) > 10


def test_get_users_metrics_df_counts(old_result, dfs):
    users_df, sessions_df, = dfs

    assert len(users_df) > 10
    assert len(sessions_df) > 10

    result_df = get_df.get_user_metrics_df(users_df, sessions_df)

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
    return utils._df_from_cache("old", user_metrics_query, conn)