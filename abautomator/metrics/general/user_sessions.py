from dataclasses import dataclass

from abautomator.metrics import BaseMetric

@dataclass
class UserSessionsMetric(BaseMetric):
    name: str = "user_sessions"
    table_name: str = "fct_user_sessions"
    table_col: str = "id"
