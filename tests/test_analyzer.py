import pytest

from abautomator import analyzer, describer
from tests import utils


@pytest.fixture
def outcomes(cleaned_desc):
    return cleaned_desc._generate_outcome_desc()


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
    assert "n_all_sessions" in result["metric"].unique()
    assert "pct_all_sessions" in result["metric"].unique()
    assert "mean" in list(result.columns)
    assert "std" in list(result.columns)
    assert "count" in list(result.columns)

    print(result.head())


def test_get_basic_confidence_intervals(analy):
    result = analy.get_basic_confidence_intervals()

    assert "upper_68_ci" in list(result.columns)
    assert "lower_95_ci" in list(result.columns)

    print(result.head())

    utils.cache_obj(result, "basic_ci")


def test_get_abs_diff_confidence_intervals(analy):
    result = analy.get_abs_diff_confidence_intervals()

    assert "mean" in list(result.columns)
    assert "std" in list(result.columns)

    utils.cache_obj(result, "abs_diff_ci")


def test_get_rel_diff_confidence_intervals(analy):
    result = analy.get_rel_diff_confidence_intervals()

    print(result)
    print(result.columns)

    assert "abs_mean" in list(result.columns)
    assert "mean" in list(result.columns)
    assert "std" in list(result.columns)

    utils.cache_obj(result, "rel_diff_ci")
