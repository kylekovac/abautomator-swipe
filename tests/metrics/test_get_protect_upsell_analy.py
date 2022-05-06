from datetime import date
import pytest
from abautomator.utils import DateRange
from abautomator import collector, describer, analyzer, metrics

from tests import utils
from tests.metrics.custom_queries import IOS_HS_ONE_QUERY, ANDROID_HS_ONE_QUERY

EXP_NAME = "ProtedtUpSellExp20224023_"
CTRL_NAME = 'ctrl'
CONDS = [
    'ProtedtUpSellExp20224023_ctrl',
    'ProtedtUpSellExp20224023_tx_w_protect_upsell',
]
EVENT = "segment_viewed_feed_item_cohorted"
EVENT_PROP = "context_homescreen_curated_cards_config_001"
DT_RANGE = DateRange(date(2022, 4, 23))

@pytest.mark.build
def test_get_analy(local_coll):
    
    local_coll.collect_data()
    assert len(local_coll.metrics) > 0
    assert len(local_coll.metrics[0].user_metric_df) > 0

    local_coll.engine = None
    utils.cache_obj(local_coll, f"{EXP_NAME}_coll")

    # for metric in local_coll.metrics:
    #     metric.user_metric_df = metric.user_metric_df[metric.user_metric_df["device_type"] == 'android']

    # print("describing data")
    # # init and run the describer
    # desc = describer.Describer(
    #     metrics=local_coll.metrics
    # )
    # outcomes_dict = desc.describe_data(exp_name=EXP_NAME)

    # print("analyzing data")
    # analy =  analyzer.Analyzer(
    #     outcomes=outcomes_dict,
    #     ctrl_name=CTRL_NAME,
    # )
    # utils.cache_obj(analy, f"{EXP_NAME}_analy")

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

            # Feed Share Breakdown

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
