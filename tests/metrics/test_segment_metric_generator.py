import pytest
import sqlalchemy

from abautomator.utils import DateRange
from abautomator import metrics

from tests import utils


def test_basic(seg_metric_generator):

    output = seg_metric_generator.generate()

    assert len(output) > 0

def test_metric_concate(seg_metric_generator):
    test = [metrics.METRIC_LOOKUP["incident_share_attempts"], *seg_metric_generator.generate(),]

    assert isinstance(test[0], metrics.BaseMetric)
    assert not isinstance(test[0], metrics.SegMetric)
    assert isinstance(test[1], metrics.SegMetric)

def test_get_segment_query(engine, seg_getter):

    output = seg_getter._get_segment_query(
        engine, DateRange(utils.get_date_n_days_ago(3))
    )

    assert isinstance(output, sqlalchemy.sql.selectable.Select)

@pytest.fixture
def seg_getter():
    return metrics.metric_generator.SegmentGetter(
        table_name="fct_share_attempts",
        segment_col="type"
    )

def test_get_segments(engine, conn, seg_getter):

    output = seg_getter.get_segments(
        engine, conn, DateRange(utils.get_date_n_days_ago(3))
    )

    assert len(output) > 0