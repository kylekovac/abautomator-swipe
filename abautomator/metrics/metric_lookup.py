from abautomator.metrics.general import incident_views, user_sessions


METRIC_LOOKUP = {
    "Incident Views": incident_views.IncidentViewsMetric(),
    "User Sessions": user_sessions.UserSessionsMetric(),
}