from sqlalchemy.sql import selectable
import pytest
import pandas as pd

def test_get_users_query(users_query):
    assert isinstance(users_query, selectable.Select)

def test_get_metric_query(sessions_query):
    assert isinstance(sessions_query, selectable.Select)

def test_populate_users_df(coll, conn):

    coll._populate_users_df(conn)

    assert len(coll.users_df) > 10
    assert "exp_cond" in list(coll.users_df.columns)
    ctrl_cond = "Dec1021InspirationMomentFinalControl"
    assert ctrl_cond in coll.users_df["exp_cond"].unique()

    pd.set_option('display.max_colwidth', None)
    print(coll.users_df.head())
