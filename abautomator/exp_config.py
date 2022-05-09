from datetime import date
from abautomator.utils import DateRange


EXP_NAME = "ProtedtUpSellExp20224023_"
CTRL_NAME = 'ctrl'
COND_ORDER = ["tx_w_protect_upsell"]
CONDS = [
    'ProtedtUpSellExp20224023_ctrl',
    'ProtedtUpSellExp20224023_tx_w_protect_upsell',
]
EVENT = "segment_viewed_feed_item_cohorted"
EVENT_PROP = "context_homescreen_curated_cards_config_001"
DT_RANGE = DateRange(date(2022, 4, 23))

PRIMARY_METRIC_LIST = [
    'n_feed_views',
    'pct_feed_views',
    'n_feed_taps',
    'pct_feed_taps',
    'n_all_feed_shares',
    'pct_all_feed_shares',
    'n_direct_feed_shares',
    'pct_direct_feed_shares',
    'n_indirect_feed_shares',
    'pct_indirect_feed_shares',
    #  'n_signup_activation',
    'pct_signup_activation',
    'n_trial_starts',
    'n_protect_cancellations',
    'n_protect_payment_successful',
]
 
SECONDARY_METRIC_LIST = [
    'n_all_sessions',
    'pct_all_sessions',
    'n_organic_sessions',
    'pct_organic_sessions',
    'n_push_driven_sessions',
    'pct_push_driven_sessions',
    'n_incident_views',
    'pct_incident_views',
    'n_incident_share_attempts',
    'pct_incident_share_attempts',
]

GUARDRAIL_METRIC_LIST = [
    'n_chats',
    'pct_chats',
    'n_friend_invites',
    'pct_friend_invites',
    'n_trial_starts',
    'pct_trial_starts',
]