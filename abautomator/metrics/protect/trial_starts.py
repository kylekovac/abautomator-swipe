from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
from sqlalchemy.sql.functions import coalesce

from abautomator.metrics import BaseMetric
from abautomator import utils


@dataclass
class TrialStartsMetric(BaseMetric):
    name: str = "trial_starts"
    table_name: str = "dim_purchased_subscriptions"
    table_col: str = "transaction_id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.transaction_id == table.c.original_transaction_id
        )

@dataclass
class ProtectPaymentSuccessfulMetric(BaseMetric):
    name: str = "protect_payment_successful"
    table_name: str = "segment_protect_landing_page_payment_successful"
    table_col: str = "id"
