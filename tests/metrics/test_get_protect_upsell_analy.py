from datetime import date
import pytest
from abautomator import collector, metrics

from tests import utils

from abautomator.exp_config import EXP_NAME, CONDS, EVENT,EVENT_PROP, DT_RANGE

@pytest.mark.build
def test_get_analy(local_coll):
    
    local_coll.collect_data()
    assert len(local_coll.metrics) > 0
    assert len(local_coll.metrics[0].user_metric_df) > 0

    local_coll.engine = None
    utils.cache_obj(local_coll, f"{EXP_NAME}_coll")


@pytest.fixture
def local_coll(engine):
    return collector.Collector(
        engine=engine,
        conds=CONDS,
        metrics=[
            # Primary metrics
            metrics.METRIC_LOOKUP["feed_views"],
            metrics.METRIC_LOOKUP["feed_taps"],
            metrics.METRIC_LOOKUP["all_feed_shares"],
            metrics.METRIC_LOOKUP["direct_feed_shares"],
            metrics.METRIC_LOOKUP["indirect_feed_shares"],
            metrics.METRIC_LOOKUP["signup_activation"],
            metrics.METRIC_LOOKUP["trial_starts"],
            metrics.METRIC_LOOKUP["protect_payment_successful"],
            metrics.METRIC_LOOKUP["protect_cancellations"],

            # Secondary metrics
            metrics.METRIC_LOOKUP["all_sessions"],
            metrics.METRIC_LOOKUP["organic_sessions"],
            metrics.METRIC_LOOKUP["push_driven_sessions"],
            metrics.METRIC_LOOKUP["incident_views"],
            metrics.METRIC_LOOKUP["incident_share_attempts"],          

            # Guardrail matrics
            metrics.METRIC_LOOKUP["chats"],
            metrics.METRIC_LOOKUP["friend_invites"],
            metrics.METRIC_LOOKUP["trial_starts"],
        ],
        event=EVENT,
        event_prop=EVENT_PROP,
        dt_range=DT_RANGE,
    )
