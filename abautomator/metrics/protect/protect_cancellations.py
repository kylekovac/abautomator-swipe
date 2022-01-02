from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
from sqlalchemy.sql.functions import coalesce

from abautomator.metrics import BaseMetric
from abautomator.collector import Collector


@dataclass
class ProtectTrialStartsMetric(BaseMetric):
    name: str = "protect_trial_starts"
    table_name: str = "dim_purchased_subscriptions"
    table_col: str = "transaction_id"

    def add_where_clause(self, query: Selectable, table: Table, coll: Collector):
        query = query.where(
            coalesce(table.c.last_cancel_datetime, table.c.last_renewal_failure_datetime) >= coll.start_dt
        )
        if coll.end_dt:
            query = query.where(
                coalesce(table.c.last_cancel_datetime, table.c.last_renewal_failure_datetime) <= coll.end_dt
            )
        return query.where(
            table.c.transaction_id == table.c.original_transaction_id
        )
