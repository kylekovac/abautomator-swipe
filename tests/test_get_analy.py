import pytest
from datetime import date

from abautomator import experiment, metrics
from abautomator.utils import DateRange
from tests import utils

@pytest.fixture
def rollback_exp():
    return experiment.Experiment(
        ctrl_name="Jan1022InspirationMomentControl",
        tx_names=["Jan1022InspirationMomentTx"],
        metrics=[
            metrics.ExpMetric("entered_phone", "pct"),
            metrics.ExpMetric("granted_contacts", "pct")
        ],
        dt_range=DateRange(date(2022, 1, 10), date(2022, 1, 15)),
    )

@pytest.mark.build
def test_get_rollback_analyzer(rollback_exp):

    coll = rollback_exp.get_collector()
    coll.collect_data()
    print(coll.metrics[0].user_metric_df.shape)

    analy = rollback_exp.get_analyzer()
    utils.cache_obj(analy, "rollback_analy")


@pytest.fixture
def inspiration_exp():
    return experiment.Experiment(
        ctrl_name="Dec1021InspirationMomentFinalControl",
        tx_names=[
            "Dec1021InspirationMomentFinalCarousel01",
            "Dec1021InspirationMomentFinalCarousel02",
            "Dec1021InspirationMomentFinalCarousel03",
            "Dec1021InspirationMomentFinalCarousel04",
            "Dec1021InspirationMomentFinalVideo01",
            "Dec1021InspirationMomentFinalvideo02",
        ],
        metrics=[
            metrics.ExpMetric("entered_phone", "pct"),
            metrics.ExpMetric("granted_contacts", "pct")
        ],
        dt_range=DateRange(date(2021, 12, 10), date(2022, 1, 4)),
        name="Dec1021InspirationMomentFinal",
    )

@pytest.mark.build
def test_get_inspiration_analyzer(inspiration_exp):

    coll = inspiration_exp.get_collector()
    coll.collect_data()
    print(coll.metrics[0].user_metric_df.shape)

    analy = inspiration_exp.get_analyzer()
    utils.cache_obj(analy, "inspiration_analy")