import pytest

from abautomator.metrics import ExpMetric

def test_name_setting():
    with pytest.raises(AssertionError):
        ExpMetric("invalid_name", "n")
    
    ExpMetric("trial_starts", "n")

def test_state_setting():
    with pytest.raises(AssertionError):
        ExpMetric("trial_starts", "invalid state")
    
    ExpMetric("trial_starts", "n")