import pytest

import pandas as pd

from abautomator import describer

def test_get_metric_data(desc):

    print(desc.metrics[0])
    result_df = desc.metrics[0].user_metric_df
    assert len(result_df) > 10
    assert "exp_cond" in list(result_df.columns)
    assert "n_user_sessions" in list(result_df.columns)


def test_when_users_metric_df_is_none(gen_metric):
    with pytest.raises(TypeError):
        describer.Describer(
            metrics=[gen_metric]
        )

def test_when_users_metric_df_missing_pct(gen_metric, users_df):
    no_pct_or_n_df = users_df.copy()
    gen_metric.user_metric_df = no_pct_or_n_df
    _check_when_users_metric_df_missing_col(gen_metric)


def test_when_users_metric_df_missing_exp_cond(gen_metric, incident_views_df):
    no_exp_cond_df = incident_views_df.copy()
    gen_metric.user_metric_df = no_exp_cond_df
    _check_when_users_metric_df_missing_col(gen_metric)


def _check_when_users_metric_df_missing_col(metric):
    with pytest.raises(describer.InvalidColumns):
        describer.Describer(
            metrics=[metric]
        )


def test_remove_exp_name_from_exp_cond(desc, exp_name):

    metric_df = desc.metrics[0].user_metric_df
    assert exp_name in metric_df["exp_cond"][0]
    desc._clean_data_dfs(exp_name)

    assert exp_name not in metric_df["exp_cond"][0]

    print(desc.metrics[0].user_metric_df.head())

def test_generate_outcome_desc(cleaned_desc):
    assert "Control" in cleaned_desc.metrics[0].user_metric_df["exp_cond"].unique()
    result = cleaned_desc._generate_outcome_desc()

    outcome_df = result["user_sessions"]["Control"]

    assert isinstance(outcome_df, pd.DataFrame)
    assert "mean" in list(outcome_df.index)
    assert "n_user_sessions" in outcome_df.columns
