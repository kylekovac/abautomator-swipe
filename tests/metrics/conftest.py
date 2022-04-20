import pytest
from datetime import date

from abautomator.metrics.metric_generator import GroupMetricGenerator, GroupInfo
from abautomator.utils import DateRange

@pytest.fixture
def proximity_generator(engine, conn, feed_share_seg_info):
    return GroupMetricGenerator(
        engine,
        conn,
        DateRange(date(2022, 4, 13)),
        segment_info=seg_info,
    )

@pytest.fixture
def seg_metric_generator(engine, conn, seg_info):
    return GroupMetricGenerator(
        engine,
        conn,
        DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        segment_info=seg_info,
    )

@pytest.fixture
def seg_info():
    return GroupInfo(
        name="Share Attempts",
        table_name="fct_share_attempts",
        table_col="id",
        segment_col="type",
    )

@pytest.fixture
def feed_share_seg_info():
    return GroupInfo(
        name="Feed Shares",
        table_name="fct_homescreen_shares",
        table_col="id",
        segment_col="share_source",
    )