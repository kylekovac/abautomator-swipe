from datetime import date, timedelta
import os
import pickle

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select, selectable

from abautomator import main, experiment

@pytest.fixture
def engine(scope="module"):
    return create_engine(f'bigquery://{main.GCP_PROJECT_ID}')

@pytest.fixture
def conn(engine):
    return engine.connect()

def test_conn(engine, conn):
    table = Table(f"echelon.dim_groups", MetaData(bind=engine), autoload=True)

    query = select(table).where(
        getattr(table.c, "event_date") == _get_yesterday()
    )

    result = conn.execute(query).all()

    assert len(result) > 10

def _get_yesterday():
    return date.today() - timedelta(days=2)

def test_get_user_data(conn, users_query):
    
    assert isinstance(users_query, selectable.Select)

    result = main._get_query_df(users_query, conn)
    print(len(result))
    assert len(result) > 10

@pytest.fixture
def users_query(engine, exp):
    return main.get_users_query(engine, exp)

@pytest.fixture
def exp():
    return experiment.Experiment(
        ctrl_cond='Dec1021InspirationMomentFinalControl',
        tx_conds=[
            'Dec1021InspirationMomentFinalVideo01',
            'Dec1021InspirationMomentFinalVideo02',
            'Dec1021InspirationMomentFinalCarousel01',
            'Dec1021InspirationMomentFinalCarousel02',
            'Dec1021InspirationMomentFinalCarousel03',
            'Dec1021InspirationMomentFinalCarousel04',
        ],
        event="segment_signup_flow_started",
        event_prop="context_traits_onboarding_flow_001",
        start_dt=_get_yesterday(),
    )

@pytest.fixture
def sessions_query(engine, exp):
    return main.get_metric_query(engine, exp, get_sessions_metric())

@pytest.fixture
def views_query(engine, exp):
    return main.get_metric_query(engine, exp, get_incident_views_metric())

def get_sessions_metric():
    return main.Metric(
        name="User Sessions",
        table_name="fct_user_sessions",
        table_col="id",
    )

def get_incident_views_metric():
    return main.Metric(
        name="Incident Views",
        table_name="fct_incident_views",
        table_col="id",
    )

def test_get_sessions_metric(conn, sessions_query):
    assert isinstance(sessions_query, selectable.Select)

    result = main._get_query_df(sessions_query, conn)

    print(sessions_query)
    print(len(result))
    print(result.head())
    print(result.dtypes)
    assert len(result) > 10

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

@pytest.fixture
def queries(users_query, sessions_query, views_query):
    return users_query, sessions_query, views_query

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
def old_result(sessions_query, users_query):
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

