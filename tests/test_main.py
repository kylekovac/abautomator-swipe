from datetime import date, timedelta

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select, selectable



from abautomator import main, config


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
    return date.today() - timedelta(days=1)

@pytest.fixture
def users_query(engine, exp):
    return main.get_users_query(engine, exp)

@pytest.fixture
def exp():
    return main.Experiment(
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

def test_get_users_query(conn, users_query):
    assert isinstance(users_query, selectable.Select)

    result = conn.execute(users_query).all()
    print(len(result))
    assert len(result) > 10

@pytest.fixture
def metric_query(engine, exp):
    return main.get_metric_query(engine, exp, get_session_metric())

def get_session_metric():
    return main.Metric(
        table_name="fct_user_sessions",
        table_col="id",
    )


def test_get_metric_query(conn, metric_query):
    assert isinstance(metric_query, selectable.Select)

    result = conn.execute(metric_query).all()
    print(len(result))
    assert len(result) > 10


def test_get_users_metrics_df(conn, metric_query, users_query):
    old_result = _get_old_result(conn, metric_query, users_query)

    users_df =  main._get_query_df(users_query, conn)
    sessions_df =  main._get_query_df(metric_query, conn)

    assert len(users_df) > 10
    assert len(sessions_df) > 10

    result_df = main.get_user_metrics_df(users_df, sessions_df)

    assert len(result_df) > 10
    assert len(result_df) == len(users_df)
    assert len(result_df) == len(old_result)


def _get_old_result(conn, metric_query, users_query):
    users_cte = users_query.cte("users")
    session_metric_cte = metric_query.cte("sessions")
    user_metrics_query = select(
        users_cte.c.echelon_user_id, users_cte.c.cohort, session_metric_cte.c.n_events
        ).select_from(
            users_cte.join(session_metric_cte, users_cte.c.echelon_user_id == session_metric_cte.c.echelon_user_id, isouter=True)
    )
    return conn.execute(user_metrics_query).all()