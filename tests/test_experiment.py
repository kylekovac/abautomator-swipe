import pytest

from abautomator import experiment


def test_get_name(exp):
    result = exp._get_name(
        "Dec1021InspirationMomentFinalCtrl", "Dec1021InspirationMomentFinalTx",
    )
    assert result == "Dec1021InspirationMomentFinal"

    with pytest.raises(experiment.InvalidName):
        exp._get_name(
            "Dec1021InspirationMomentFinalCtrl", "Dec1021InspirationMomentFinalCtrl",
        )

    with pytest.raises(experiment.InvalidName):
        exp._get_name(
            "Dec1021InspirationMomentFinal", "Dec1021InspirationMomentFinal_OTHERISEMPTY",
        )

def test_exp_name_set(exp):
    assert exp.name == "Dec1021InspirationMomentFinal"

def test_cond_name_set(exp):
    assert exp.ctrl_cond.name == "Control"
    assert exp.tx_conds[0].name == "Video01"