from dataclasses import dataclass

from abautomator.metrics import BaseMetric

@dataclass
class UserSessionsMetric(BaseMetric):
    name: str = "User Sessions"
    table_name: str = "fct_user_sessions"
    table_col: str = "id"
