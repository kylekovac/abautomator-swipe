from datetime import date
import pytest
from abautomator.utils import DateRange
from abautomator import collector, describer, analyzer, metrics

from tests import utils
from tests.metrics.custom_queries import IOS_HS_ONE_QUERY, ANDROID_HS_ONE_QUERY


@pytest.mark.build
def test_get_android_seg_metric_analy(android_seg_metric_coll):

    android_seg_metric_coll.collect_data()
    assert len(android_seg_metric_coll.metrics) > 0
    assert len(android_seg_metric_coll.metrics[0].user_metric_df) > 0

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=android_seg_metric_coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="AndroidHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        ctrl_name='Ctrl02112022',
    )

    utils.cache_obj(analy, f"homescreen_analy_android")

@pytest.fixture
def android_seg_metric_coll(engine, group_metric_generator):
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
            *group_metric_generator.generate(),
        ],
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=ANDROID_HS_ONE_QUERY,
    )

@pytest.mark.build
def test_get_ios_seg_metric_analy(ios_seg_metric_coll):

    ios_seg_metric_coll.collect_data()
    assert len(ios_seg_metric_coll.metrics) > 0
    assert len(ios_seg_metric_coll.metrics[0].user_metric_df) > 0

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=ios_seg_metric_coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="iOSHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        ctrl_name='Ctrl02092022',
    )

    utils.cache_obj(analy, f"homescreen_analy_ios")

@pytest.fixture
def ios_seg_metric_coll(engine, group_metric_generator):
    return collector.Collector(
        engine=engine,
        conds=[
            'iOSHomescreenCtrl02092022',
            'iOSHomescreenTx02092022',
        ],
        metrics=[
            # metrics.METRIC_LOOKUP["all_sessions"],
            # metrics.METRIC_LOOKUP["organic_sessions"],
            # metrics.METRIC_LOOKUP["push_driven_sessions"],
            # metrics.METRIC_LOOKUP["incident_views"],
            metrics.METRIC_LOOKUP["incident_share_attempts"],
            *group_metric_generator.generate(),
        ],
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=IOS_HS_ONE_QUERY,
    )
