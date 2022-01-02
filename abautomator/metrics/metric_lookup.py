from abautomator.metrics.general import user_sessions, incident_views, incident_shares, friend_invites
from abautomator.metrics.protect import trial_starts


METRIC_LOOKUP = {
    "friend_invites": friend_invites.FriendInvitesMetric(),
    "incident_views": incident_views.IncidentViewsMetric(),
    "incident_shares": incident_shares.IncidentSharesMetric(),
    "user_sessions": user_sessions.UserSessionsMetric(),
    "trial_starts": trial_starts.TrialStartsMetric(),
}