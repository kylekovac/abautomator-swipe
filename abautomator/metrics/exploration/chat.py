from dataclasses import dataclass
from sqlalchemy import and_
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator import utils

@dataclass
class ChatsMetric(BaseMetric):
    name: str = "chats"
    table_name: str = "dim_incident_chats"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.is_deleted == False,
        )