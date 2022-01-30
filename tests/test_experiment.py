import pytest
from datetime import date

from abautomator import experiment, utils
from abautomator import metrics
from abautomator.utils import DateRange
from tests import utils


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
            metrics.ExpMetric("granted_location", "n"),
            metrics.ExpMetric("granted_notifs", "n"),
        ]

@pytest.fixture
def exp(tx_names, exp_metrics):
    return experiment.Experiment(
        ctrl_name="Dec1021InspirationMomentFinalControl",
        tx_names=tx_names,
        metrics=exp_metrics,
        dt_range=DateRange(utils.get_yesterday()),
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


def test_convert_exp_metrics_to_base_metrics(exp):

    result = exp._convert_exp_metrics_to_base_metrics()
    assert isinstance(result[0], metrics.BaseMetric)
    assert len(result) == 2

    exp.metrics = exp_metrics_one_drop()
    result = exp._convert_exp_metrics_to_base_metrics()
    assert isinstance(result[0], metrics.BaseMetric)
    assert len(result) == 2


def exp_metrics_one_drop():
    return [
            metrics.ExpMetric("granted_location", "n"),
            metrics.ExpMetric("granted_location", "pct"),
            metrics.ExpMetric("granted_notifs", "n"),
        ]
