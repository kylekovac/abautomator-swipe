import pytest
from sqlalchemy import create_engine

from abautomator import config, experiment, get_query, metric, collector
from tests import utils

@pytest.fixture
def engine(scope="module"):
    return create_engine(f'bigquery://{config.GCP_PROJECT_ID}')

@pytest.fixture
def conn(engine):
    return engine.connect()

@pytest.fixture
def queries(users_query, sessions_query, views_query):
    return users_query, sessions_query, views_query

@pytest.fixture
def users_query(coll):
    return coll._get_users_query()

@pytest.fixture
def coll(engine, cond_strs, sessions_metric):
    return collector.Collector(
        engine=engine,
        conds=cond_strs,
        metrics=[sessions_metric],
        event="segment_signup_flow_started",
        event_prop="context_traits_onboarding_flow_001",
        start_dt=utils._get_yesterday(),
    )

@pytest.fixture
def coll_two_metric(coll, metrics_list):
    coll.metrics = metrics_list
    return coll

@pytest.fixture
def coll_w_users_df(coll, users_df):
    coll.users_df = users_df
    return coll

@pytest.fixture
def cond_strs():
    return [
        "Dec1021InspirationMomentFinalVideo01",
        "Dec1021InspirationMomentFinalVideo02",
        "Dec1021InspirationMomentFinalCarousel01",
        "Dec1021InspirationMomentFinalCarousel02",
        "Dec1021InspirationMomentFinalCarousel03",
        "Dec1021InspirationMomentFinalCarousel04",
    ]

@pytest.fixture
def sessions_query(coll, sessions_metric):
    return coll._get_metric_query(sessions_metric)

@pytest.fixture
def views_query(coll, incident_views_metric):
    return coll._get_metric_query(incident_views_metric)

@pytest.fixture
def exp(ctrl_cond, tx_conds, metrics_list):
    return experiment.Experiment(
        ctrl_cond=ctrl_cond,
        tx_conds=tx_conds,
        metrics=metrics_list,
        event="segment_signup_flow_started",
        event_prop="context_traits_onboarding_flow_001",
        start_dt=utils._get_yesterday(),
    )

@pytest.fixture
def ctrl_cond():
    return experiment.Condition("Dec1021InspirationMomentFinalControl")

@pytest.fixture
def tx_conds():
    return [
        experiment.Condition("Dec1021InspirationMomentFinalVideo01"),
        experiment.Condition("Dec1021InspirationMomentFinalVideo02"),
        experiment.Condition("Dec1021InspirationMomentFinalCarousel01"),
        experiment.Condition("Dec1021InspirationMomentFinalCarousel02"),
        experiment.Condition("Dec1021InspirationMomentFinalCarousel03"),
        experiment.Condition("Dec1021InspirationMomentFinalCarousel04"),
    ]

@pytest.fixture
def sessions_metric():
    return metric.Metric(
        name="User Sessions",
        table_name="fct_user_sessions",
        table_col="id",
    )

@pytest.fixture
def incident_views_metric():
    return metric.Metric(
        name="Incident Views",
        table_name="fct_incident_views",
        table_col="id",
    )

@pytest.fixture
def metrics_list(sessions_metric, incident_views_metric):
    return [sessions_metric, incident_views_metric]

@pytest.fixture
def dfs(users_df, sessions_df):
    return users_df, sessions_df

@pytest.fixture
def users_df(conn, users_query):
    return utils._df_from_cache("users", users_query, conn)

@pytest.fixture
def sessions_df(conn, sessions_query):
    return utils._df_from_cache("sessions", sessions_query, conn)