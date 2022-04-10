from cmath import tan
import pytest
import sqlalchemy
from abautomator.metrics.metric_generator import SegMetricGenerator, SegmentGetter, SegmentInfo
from abautomator.utils import DateRange

from tests import utils


def test_basic(engine, conn, seg_getter, seg_info):

    gen = SegMetricGenerator(
        engine,
        conn,
        DateRange(utils.get_yesterday()),
        segment_info=seg_info,
        segment_getter=seg_getter,
    )
    output = gen.generate()

    assert len(output) > 0

@pytest.fixture
def seg_info():
    return SegmentInfo(
        name="Incident Share Attempts",
        table_name="fct_share_attempts",
        table_col="id",
        segment_col="general_type",
    )


@pytest.fixture
def seg_getter():
    return SegmentGetter(
        table_name="fct_share_attempts",
        segment_col="general_type"
    )

# segmented_metrics tests
def test_get_segment_query(engine, seg_getter):

    output = seg_getter._get_segment_query(
        engine, DateRange(utils.get_yesterday())
    )

    assert isinstance(output, sqlalchemy.sql.selectable.Select)

def test_get_segments(engine, conn, seg_getter):

    output = seg_getter.get_segments(
        engine, conn, DateRange(utils.get_yesterday())
    )

    assert len(output) > 0
