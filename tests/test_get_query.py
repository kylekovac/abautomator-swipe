import pytest
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select, selectable

from abautomator import main
from tests import utils


def test_conn(engine, conn):
    table = Table(f"echelon.dim_groups", MetaData(bind=engine), autoload=True)

    query = select(table).where(
        getattr(table.c, "event_date") == utils._get_yesterday()
    )

    result = conn.execute(query).all()

    assert len(result) > 10

def test_get_user_data(conn, users_query):
    
    assert isinstance(users_query, selectable.Select)

    result = main._get_query_df(users_query, conn)
    print(len(result))
    assert len(result) > 10

def test_get_sessions_metric(conn, sessions_query):
    assert isinstance(sessions_query, selectable.Select)

    result = main._get_query_df(sessions_query, conn)

    print(sessions_query)
    print(len(result))
    print(result.head())
    print(result.dtypes)
    assert len(result) > 10