from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator import utils


@dataclass
class AllSessionsMetric(BaseMetric):
    name: str = "all_sessions"
    table_name: str = "fct_user_sessions"
    table_col: str = "id"

@dataclass
class OrganicSessionsMetric(AllSessionsMetric):
    name: str = "organic_sessions"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_time_frame(query, table, dt_range)
        return query.where(
            table.c.is_push_driven == False
        )

@dataclass
class PushDrivenSessionsMetric(AllSessionsMetric):
    name: str = "push_driven_sessions"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_time_frame(query, table, dt_range)
        return query.where(
            table.c.is_push_driven == True
        )