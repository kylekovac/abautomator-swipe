import os
import pickle
import pytest

from abautomator import analyzer, describer


@pytest.fixture
def outcomes(cleaned_trans):
    return cleaned_trans._generate_outcome_desc()

@pytest.fixture
def analy(outcomes):
    return analyzer.Analyzer(
        outcomes=outcomes,
        ctrl_name="Control"
    )

def test_consolidate_descriptions(analy):

    analy._consolidate_descriptions()
    result = analy.base_df

    assert "Control" in result["exp_cond"].unique()
    assert "Video01" in result["exp_cond"].unique()
    assert "n_user_sessions" in result["metric"].unique()
    assert "pct_user_sessions" in result["metric"].unique()
    assert "mean" in list(result.columns)
    assert "std" in list(result.columns)
    assert "count" in list(result.columns)

    print(result.head())

def test_add_basic_confidence_intervals(analy):
    analy._consolidate_descriptions()
    result = analy._add_basic_confidence_intervals()

    assert "upper_68_ci" in list(result.columns)
    assert "lower_95_ci" in list(result.columns)

    print(result.head())

    pickle.dump(
        result, open(os.path.join("tests", f"data_desc.p"), "wb" )
    )

def test_add_abs_diff_confidence_intervals(analy):
    analy._consolidate_descriptions()
    result = analy._add_abs_diff_confidence_intervals()
