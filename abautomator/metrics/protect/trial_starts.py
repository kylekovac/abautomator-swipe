from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
from sqlalchemy.sql.functions import coalesce

from abautomator.metrics import BaseMetric
from abautomator.collector import Collector
from abautomator import utils


@dataclass
class TrialStartsMetric(BaseMetric):
    name: str = "trial_starts"
    table_name: str = "dim_purchased_subscriptions"
    table_col: str = "transaction_id"

    def add_where_clause(self, query: Selectable, table: Table, coll: Collector):
        query = utils.add_time_frame(query, table, coll.dt_range)
        return query.where(
            table.c.transaction_id == table.c.original_transaction_id
        )
