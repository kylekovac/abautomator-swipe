from abautomator.metrics.general import user_sessions, incident_views, incident_shares, friend_invites
from abautomator.metrics.protect import trial_starts, protect_cancellations
from abautomator.metrics.exploration import feed
from abautomator.metrics.activation import (
    granted_location, entered_phone, granted_notifs, signup_complete, granted_contacts,
    viewed_shs,
)


METRIC_LOOKUP = {
    # general
    "friend_invites": friend_invites.FriendInvitesMetric(),

    "incident_share_completes": incident_shares.IncidentShareCompletesMetric(),
    "incident_share_attempts": incident_shares.IncidentShareAttemptsMetric(),
    "incident_views": incident_views.IncidentViewsMetric(),

    "all_sessions": user_sessions.AllSessionsMetric(),
    "organic_sessions": user_sessions.OrganicSessionsMetric(),
    "push_driven_sessions": user_sessions.PushDrivenSessionsMetric(),

    # explore
    "feed_views": feed.FeedViewsMetric(),
    "feed_taps": feed.FeedTapsMetric(),
    "all_feed_shares": feed.AllFeedSharesMetric(),
    "direct_feed_shares": feed.DirectFeedSharesMetric(),
    "indirect_feed_shares": feed.IndirectFeedSharesMetric(),
    
    # protect
    "protect_cancellations" : protect_cancellations.ProtectCancellationsMetric(),
    "trial_starts": trial_starts.TrialStartsMetric(),

    # activation
    "granted_location": granted_location.GrantedLocationMetric(),
    "entered_phone": entered_phone.EnteredPhoneMetric(),
    "granted_notifs": granted_notifs.GrantedNotifsMetric(),
    "signup_complete": signup_complete.SignupCompleteMetric(),
    "granted_contacts": granted_contacts.GrantedContactsMetric(),
    "viewed_SHS": viewed_shs.ViewedShsMetric(),

}
