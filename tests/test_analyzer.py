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

    result = analy._consolidate_descriptions()

    assert "Control" in result["exp_cond"].unique()
    assert "Video01" in result["exp_cond"].unique()
    assert "n_user_sessions" in result["metric"].unique()
    assert "pct_user_sessions" in result["metric"].unique()
    assert "est_mean" in list(result.columns)
    assert "est_std" in list(result.columns)
    assert "est_count" in list(result.columns)

    print(result.head())

def test_add_confidence_intervals(analy):
    pass