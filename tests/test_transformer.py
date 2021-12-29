import os
import pickle
import pytest

from abautomator import transformer

@pytest.fixture
def trans(coll_w_users_df):
    try:
        return pickle.load(
            open(os.path.join("tests", f"transformer.p"), "rb" )
        )
    except FileNotFoundError:
        coll_w_users_df.collect_data()
        trans = transformer.Transformer(
            metrics=coll_w_users_df.metrics
        )
        pickle.dump(
            trans, open(os.path.join("tests", f"transformer.p"), "wb" )
        )
        return trans

def test_get_metric_data(trans):

    print(trans.metrics[0])
    result_df = trans.metrics[0].data_df
    assert len(result_df) > 10
    assert "exp_cond" in list(result_df.columns)
    assert "n_user_sessions" in list(result_df.columns)

def test_column_check(sessions_metric, users_df):
    with pytest.raises(TypeError):
        transformer.Transformer(
            metrics=[sessions_metric]
        )

    sessions_metric.data_df = users_df
    with pytest.raises(transformer.InvalidColumns):
        transformer.Transformer(
            metrics=[sessions_metric]
        )

def test_remove_exp_name_from_exp_cond(trans):

    exp_name = "Dec1021InspirationMomentFinal"

    metric_df = trans.metrics[0].data_df
    assert exp_name in metric_df["exp_cond"][0]
    trans._clean_data_dfs(exp_name)

    assert exp_name not in metric_df["exp_cond"][0]

    print(trans.metrics[0].data_df.head())
