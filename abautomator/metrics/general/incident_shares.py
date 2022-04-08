from dataclasses import dataclass
from sqlalchemy import or_
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator import utils

@dataclass
class IncidentShareCompletesMetric(BaseMetric):
    name: str = "incident_share_completes"
    table_name: str = "fct_share_completes_installs"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.general_type == "Incident Shares"
        )

@dataclass
class IncidentShareAttemptsMetric(BaseMetric):
    name: str = "incident_share_attempts"
    table_name: str = "fct_share_attempts"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            or_(
                table.c.general_type == "Screenshot",
                table.c.general_type.contains('Shared Button')
            )
        )