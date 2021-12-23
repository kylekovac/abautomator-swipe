from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select, selectable

import pytest

from abautomator import main, config


@pytest.fixture
def engine(scope="module"):
    return create_engine(f'bigquery://{main.GCP_PROJECT_ID}')

@pytest.fixture
def connection(engine):
    return engine.connect()

def exp_config():
    return {
        "EXP_START": date(2021, 12, 10),
        "EXP_END": None,
        "DEVICES": ["android", "ios"],
        "COHORTING_PROP": "context_traits_onboarding_flow_001",
        "COHORTING_TABLE": "segment_signup_flow_started",
        "COHORT_NAMES": [
            'Dec1021InspirationMomentFinalVideo01',
            'Dec1021InspirationMomentFinalVideo02',
            'Dec1021InspirationMomentFinalCarousel01',
            'Dec1021InspirationMomentFinalCarousel02',
            'Dec1021InspirationMomentFinalCarousel03',
            'Dec1021InspirationMomentFinalCarousel04',
            'Dec1021InspirationMomentFinalControl',
        ],
    }

def get_yesterday():
    return date.today() - timedelta(days=1)

# def test_connection(engine, connection):
#     table = Table(f"echelon.dim_groups", MetaData(bind=engine), autoload=True)

#     query = select(table).where(
#         getattr(table.c, "event_date") == get_yesterday()
#     )

#     result = connection.execute(query).all()

#     assert len(result) > 10

def test_get_users(engine, connection):
    query = main.get_users(engine, exp_config())
    assert isinstance(query, selectable.Select)

    result = connection.execute(query).all()
    assert len(result) > 10




