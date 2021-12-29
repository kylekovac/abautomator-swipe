import os
import pickle
import pytest

import pandas as pd

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

@pytest.fixture
def exp_name():
    return "Dec1021InspirationMomentFinal"

def test_remove_exp_name_from_exp_cond(trans, exp_name):

    metric_df = trans.metrics[0].data_df
    assert exp_name in metric_df["exp_cond"][0]
    trans._clean_data_dfs(exp_name)

    assert exp_name not in metric_df["exp_cond"][0]

    print(trans.metrics[0].data_df.head())

@pytest.fixture
def cleaned_trans(trans, exp_name):
    trans._clean_data_dfs(exp_name)
    return trans

def test_generate_outcome_desc(cleaned_trans):
    assert "Control" in cleaned_trans.metrics[0].data_df["exp_cond"].unique()
    result = cleaned_trans._generate_outcome_desc()

    outcome_df = result["User Sessions"]["Control"]

    assert isinstance(outcome_df, pd.DataFrame)
    assert "mean" in list(outcome_df.index)
    assert "n_user_sessions" in outcome_df.columns
