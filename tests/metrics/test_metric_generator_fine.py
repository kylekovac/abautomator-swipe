from datetime import date
import pytest
import sqlalchemy
from abautomator.metrics.metric_generator import SegMetricGenerator, SegmentGetter, SegmentInfo
from abautomator.utils import DateRange
from abautomator import collector, describer, analyzer, metrics

from tests import utils
from tests.test_get_hs_one import CUSTOM_QUERIES


def test_basic(seg_metric_generator):

    output = seg_metric_generator.generate()

    assert len(output) > 0

@pytest.fixture
def seg_metric_generator(engine, conn, seg_info):
    return SegMetricGenerator(
        engine,
        conn,
        DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        segment_info=seg_info,
    )

@pytest.fixture
def seg_info():
    return SegmentInfo(
        name="Share Attempts",
        table_name="fct_share_attempts",
        table_col="id",
        segment_col="type",
    )

def test_use_android_seg_metric(android_seg_metric_coll):

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

    utils.cache_obj(analy, f"homescreen_analy_android_fine")

@pytest.fixture
def android_seg_metric_coll(engine, seg_metric_generator):
    return collector.Collector(
        engine=engine,
        conds=[
            'AndroidHomescreenCtrl02112022',
            'AndroidHomescreenTx02112022',
        ],
        metrics=[
            metrics.METRIC_LOOKUP["incident_share_attempts"],
            *seg_metric_generator.generate(),
        ],
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=CUSTOM_QUERIES['android'],
    )

def test_use_ios_seg_metric(ios_seg_metric_coll):

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

    utils.cache_obj(analy, f"homescreen_analy_ios_fine")

@pytest.fixture
def ios_seg_metric_coll(engine, seg_metric_generator):
    return collector.Collector(
        engine=engine,
        conds=[
            'iOSHomescreenCtrl02092022',
            'iOSHomescreenTx02092022',
        ],
        metrics=[
            metrics.METRIC_LOOKUP["incident_share_attempts"],
            *seg_metric_generator.generate(),
        ],
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=CUSTOM_QUERIES['ios'],
    )

def test_metric_concate(seg_metric_generator):
    test = [metrics.METRIC_LOOKUP["incident_share_attempts"], *seg_metric_generator.generate(),]
    for item in test:
        print(item)

# segmented_metrics tests
def test_get_segment_query(engine, seg_getter):

    output = seg_getter._get_segment_query(
        engine, DateRange(utils.get_yesterday())
    )

    assert isinstance(output, sqlalchemy.sql.selectable.Select)

@pytest.fixture
def seg_getter():
    return SegmentGetter(
        table_name="fct_share_attempts",
        segment_col="type"
    )

def test_get_segments(engine, conn, seg_getter):

    output = seg_getter.get_segments(
        engine, conn, DateRange(utils.get_yesterday())
    )

    assert len(output) > 0
