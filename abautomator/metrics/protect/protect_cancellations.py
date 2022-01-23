from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
from sqlalchemy.sql.functions import coalesce

from abautomator import utils
from abautomator.metrics import BaseMetric


@dataclass
class ProtectCancellationsMetric(BaseMetric):
    name: str = "protect_cancellations"
    table_name: str = "dim_purchased_subscriptions"
    table_col: str = "transaction_id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = query.where(
            coalesce(table.c.last_cancel_datetime, table.c.last_renewal_failure_datetime) >= dt_range.start
        )
        if dt_range.end:
            query = query.where(
                coalesce(table.c.last_cancel_datetime, table.c.last_renewal_failure_datetime) <= dt_range.end
            )
        return query
