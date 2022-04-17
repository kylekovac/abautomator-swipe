import pytest
from datetime import date

from abautomator.metrics.metric_generator import SegMetricGenerator, SegmentInfo
from abautomator.utils import DateRange

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