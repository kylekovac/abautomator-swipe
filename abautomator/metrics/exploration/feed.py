from dataclasses import dataclass
from sqlalchemy import or_
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator import utils

@dataclass
class FeedImpressionsMetric(BaseMetric):
    name: str = "feed_impresssions"
    table_name: str = "segment_viewed_feed_item"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.section.contains("forYou", "mostImportant")
        )

@dataclass
class FeedTapsMetric(BaseMetric):
    name: str = "feed_taps"
    table_name: str = "segment_tapped_feed_item"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.section.contains("forYou", "mostImportant")
        )

@dataclass
class FeedSharesMetric(BaseMetric):
    name: str = "feed_shares"
    table_name: str = "segment_shared_feed_item"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.section.contains("forYou", "mostImportant")
        )
