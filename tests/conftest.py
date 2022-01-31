import pickle
import pytest
from sqlalchemy import create_engine

from abautomator import config, collector, describer
from abautomator.utils import DateRange
from abautomator.metrics import METRIC_LOOKUP
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
        dt_range=DateRange(utils.get_yesterday()),
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
        "Dec1021InspirationMomentFinalControl",
        "Dec1021InspirationMomentFinalVideo01",
        "Dec1021InspirationMomentFinalVideo02",
        "Dec1021InspirationMomentFinalCarousel01",
        "Dec1021InspirationMomentFinalCarousel02",
        "Dec1021InspirationMomentFinalCarousel03",
        "Dec1021InspirationMomentFinalCarousel04",
    ]

@pytest.fixture
def incident_views_query(coll, incident_views_metric):
    return incident_views_metric._get_metric_query(coll.engine, coll.dt_range)

@pytest.fixture
def sessions_query(coll, sessions_metric):
    return sessions_metric._get_metric_query(coll.engine, coll.dt_range)

@pytest.fixture
def views_query(coll, incident_views_metric):
    return incident_views_metric._get_metric_query(coll.engine, coll.dt_range)

@pytest.fixture
def gen_metric(incident_views_metric):
    return incident_views_metric

@pytest.fixture
def sessions_metric():
    return METRIC_LOOKUP["user_sessions"]

@pytest.fixture
def friend_invite_metric():
    return METRIC_LOOKUP["friend_invites"]

@pytest.fixture
def incident_views_metric():
    return METRIC_LOOKUP["incident_views"]

@pytest.fixture
def metrics_list(sessions_metric, incident_views_metric):
    return [sessions_metric, incident_views_metric]

@pytest.fixture
def dfs(users_df, sessions_df):
    return users_df, sessions_df

@pytest.fixture
def incident_views_df(conn, incident_views_query):
    return utils.df_from_cache("incident_views", incident_views_query, conn)

@pytest.fixture
def users_df(conn, users_query):
    return utils.df_from_cache("users", users_query, conn)

@pytest.fixture
def sessions_df(conn, sessions_query):
    return utils.df_from_cache("sessions", sessions_query, conn)

@pytest.fixture
def exp_name():
    return "Dec1021InspirationMomentFinal"

@pytest.fixture
def desc(coll_w_users_df):
    try:
        return pickle.load(
            open(utils.get_cache_path("describer"), "rb" )
        )
    except FileNotFoundError:
        coll_w_users_df.collect_data()
        desc = describer.Describer(
            metrics=coll_w_users_df.metrics
        )
        utils.cache_obj(desc, "desc")

        return desc

@pytest.fixture
def cleaned_desc(desc, exp_name):
    desc._clean_data_dfs(exp_name)
    return desc


def pytest_addoption(parser):
    # https://stackoverflow.com/questions/40880259/how-to-pass-arguments-in-pytest-by-command-line
    parser.addoption("--name", action="store", default="default name")

    # https://stackoverflow.com/questions/47559524/pytest-how-to-skip-tests-unless-you-declare-an-option-flag
    parser.addoption(
        "--runbuild", action="store_true", default=False, help="run slow tests"
    )

# name flag accessory function
def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.name
    if 'name' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("name", [option_value])

# name flag accessory function
def pytest_configure(config):
    config.addinivalue_line("markers", "build: mark test as building things")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runbuild"):
        # --runbuild given in cli: do not skip build tests
        return
    skip_slow = pytest.mark.skip(reason="need --runbuild option to run")
    for item in items:
        if "build" in item.keywords:
            item.add_marker(skip_slow)