import pytest

import pandas as pd

from abautomator import describer

def test_get_metric_data(desc):

    print(desc.metrics[0])
    result_df = desc.metrics[0].data_df
    assert len(result_df) > 10
    assert "exp_cond" in list(result_df.columns)
    assert "n_user_sessions" in list(result_df.columns)

def test_column_check(sessions_metric, users_df):
    with pytest.raises(TypeError):
        describer.Describer(
            metrics=[sessions_metric]
        )

    sessions_metric.data_df = users_df
    with pytest.raises(describer.InvalidColumns):
        describer.Describer(
            metrics=[sessions_metric]
        )

def test_remove_exp_name_from_exp_cond(desc, exp_name):

    metric_df = desc.metrics[0].data_df
    assert exp_name in metric_df["exp_cond"][0]
    desc._clean_data_dfs(exp_name)

    assert exp_name not in metric_df["exp_cond"][0]

    print(desc.metrics[0].data_df.head())

def test_generate_outcome_desc(cleaned_desc):
    assert "Control" in cleaned_desc.metrics[0].data_df["exp_cond"].unique()
    result = cleaned_desc._generate_outcome_desc()

    outcome_df = result["User Sessions"]["Control"]

    assert isinstance(outcome_df, pd.DataFrame)
    assert "mean" in list(outcome_df.index)
    assert "n_user_sessions" in outcome_df.columns
