
from abautomator import utils

def test_get_df_from_query(users_query, conn):
    result = utils.get_df_from_query(users_query, conn)
    assert len(result) > 10