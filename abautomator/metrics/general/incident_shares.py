from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator.collector import Collector
from abautomator import utils

@dataclass
class IncidentSharesMetric(BaseMetric):
    name: str = "incident_shares"
    table_name: str = "fct_share_completes_installs"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, coll: Collector):
        query = utils.add_time_frame(query, table, coll.dt_range)
        return query.where(
            table.c.general_type == "Incident Shares"
        )
