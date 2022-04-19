from datetime import date
import pytest
from abautomator.utils import DateRange
from abautomator import collector, describer, analyzer, metrics

from tests import utils
from tests.metrics.custom_queries import IOS_HS_ONE_QUERY, ANDROID_HS_ONE_QUERY


@pytest.mark.build
def test_get_proximity_analy(proximity_coll):

    proximity_coll.collect_data()
    assert len(proximity_coll.metrics) > 0
    assert len(proximity_coll.metrics[0].user_metric_df) > 0

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=proximity_coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="AndroidHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        ctrl_name='Ctrl02112022',
    )

    utils.cache_obj(analy, f"homescreen_analy_android")

@pytest.fixture
def proximity_coll(engine):
    return collector.Collector(
        engine=engine,
        conds=[
            'AndroidHomescreenCtrl02112022',
            'AndroidHomescreenTx02112022',
        ],
        metrics=[
            # metrics.METRIC_LOOKUP["all_sessions"],
            # metrics.METRIC_LOOKUP["organic_sessions"],
            # metrics.METRIC_LOOKUP["push_driven_sessions"],
            # metrics.METRIC_LOOKUP["incident_views"],
            metrics.METRIC_LOOKUP["incident_share_attempts"],
        ],
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=ANDROID_HS_ONE_QUERY,
    )
