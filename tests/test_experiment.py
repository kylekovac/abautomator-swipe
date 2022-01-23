import pytest

from abautomator import experiment, utils
from abautomator.metrics import METRIC_LOOKUP
from tests.utils import get_yesterday


@pytest.fixture
def tx_names():
    return [
        "Dec1021InspirationMomentFinalVideo01",
        "Dec1021InspirationMomentFinalVideo02",
        "Dec1021InspirationMomentFinalCarousel01",
        "Dec1021InspirationMomentFinalCarousel02",
        "Dec1021InspirationMomentFinalCarousel03",
        "Dec1021InspirationMomentFinalCarousel04",
    ]

@pytest.fixture
def exp_metrics():
    return [
            METRIC_LOOKUP["granted_location"],
            METRIC_LOOKUP["granted_notifs"],
        ]

@pytest.fixture
def exp(tx_names, exp_metrics):
    return experiment.Experiment(
        ctrl_name="Dec1021InspirationMomentFinalControl",
        tx_names=tx_names,
        metrics=exp_metrics,
        start_dt=utils.get_yesterday()
    )

def test_init(exp):
    exp.get_collector()

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
