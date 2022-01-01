from dataclasses import dataclass

from abautomator.metrics import BaseMetric

@dataclass
class IncidentViewsMetric(BaseMetric):
    name: str = "Incident Views"
    table_name: str = "fct_incident_views"
    table_col: str = "id"
