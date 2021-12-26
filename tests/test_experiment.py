import pytest

from abautomator import experiment

def test_get_name(exp):
    result = exp._get_name(exp.ctrl_cond, exp.tx_conds[0])
    assert result == "Dec1021InspirationMomentFinal"

    with pytest.raises(experiment.InvalidName):
        exp._get_name(exp.ctrl_cond, exp.ctrl_cond)

    with pytest.raises(experiment.InvalidName):
        exp._get_name(exp.ctrl_cond, exp.ctrl_cond + "onecondempty")

def test_exp_name_set(exp):
    assert exp.name == "Dec1021InspirationMomentFinal"


