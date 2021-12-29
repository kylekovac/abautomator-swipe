from sqlalchemy.sql import select, selectable

def test_get_users_query(users_query):
    assert isinstance(users_query, selectable.Select)

def test_get_metric_query(sessions_query):
    assert isinstance(sessions_query, selectable.Select)

def test_populate_users_df(coll, conn):

    coll._populate_users_df(conn)

    print(coll.users_df)
    assert len(coll.users_df) > 10
    assert "exp_cond" in list(coll.users_df.columns)
    ctrl_cond = "Dec1021InspirationMomentFinalControl"
    assert ctrl_cond in coll.users_df["exp_cond"].unique()

def test_add_exp_cond_to_metric(coll_w_users_df, sessions_df):
    result_df = coll_w_users_df._add_exp_cond_to_metric(sessions_df)

    assert len(result_df) > 10
    assert len(result_df.columns) > len(coll_w_users_df.users_df.columns)
    assert len(result_df.columns) > len(sessions_df.columns)

def test_populate_metric_data_df(coll_w_users_df, conn):
    coll_w_users_df._populate_metric_data_dfs(conn)

    result_df = coll_w_users_df.metrics[0].data_df
    assert len(result_df) > 10
    assert len(result_df.columns) > len(coll_w_users_df.users_df.columns)
    assert "exp_cond" in list(result_df.columns)
    assert "n_user_sessions" in list(result_df.columns)
