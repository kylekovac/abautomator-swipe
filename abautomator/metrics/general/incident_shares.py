from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric

@dataclass
class IncidentSharesMetric(BaseMetric):
    name: str = "Incident Shares"
    table_name: str = "fct_share_completes_installs"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table):
        return query.where(
            table.c.general_type == "Incident Shares"
        )
