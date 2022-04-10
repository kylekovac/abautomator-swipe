from datetime import date
import pytest
import sqlalchemy
from abautomator.metrics.metric_generator import SegMetricGenerator, SegmentGetter, SegmentInfo
from abautomator.utils import DateRange
from abautomator import collector, describer, analyzer

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
        DateRange(utils.get_yesterday()),
        segment_info=seg_info,
    )

@pytest.fixture
def seg_info():
    return SegmentInfo(
        name="Incident Share Attempts",
        table_name="fct_share_attempts",
        table_col="id",
        segment_col="general_type",
    )


def test_use_seg_metric(seg_metric_coll):

    seg_metric_coll.collect_data()
    assert len(seg_metric_coll.metrics) > 0
    assert len(seg_metric_coll.metrics[0].user_metric_df) > 0

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=seg_metric_coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="AndroidHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        # ctrl_name=self.ctrl_name.replace(self.name, ""),
        ctrl_name='Ctrl02112022',
    )

    utils.cache_obj(analy, f"homescreen_analy_android")

@pytest.fixture
def seg_metric_coll(engine, seg_metric_generator):
    return collector.Collector(
        engine=engine,
        conds=[
            'AndroidHomescreenCtrl02112022',
            'AndroidHomescreenTx02112022',
        ],
        metrics=seg_metric_generator.generate(),
        event="segment_app_open_2",
        event_prop="context_traits_homescreen_v_1_001",
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=CUSTOM_QUERIES['android'],
    )

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
        segment_col="general_type"
    )

def test_get_segments(engine, conn, seg_getter):

    output = seg_getter.get_segments(
        engine, conn, DateRange(utils.get_yesterday())
    )

    assert len(output) > 0
