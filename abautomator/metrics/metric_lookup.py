from abautomator.metrics.general import incident_views, user_sessions


METRIC_LOOKUP = {
    "incident_views": incident_views.IncidentViewsMetric(),
    "user_sessions": user_sessions.UserSessionsMetric(),
}