from dataclasses import dataclass

from abautomator.metrics import BaseMetric
from abautomator import utils


@dataclass
class GroupMetric(BaseMetric):
    segment_col: str = None
    segment_value: str = None

    def add_where_clause(self, query, table, dt_range):
        query = query.where(
            getattr(table.c, self.segment_col) == self.segment_value
        )
        return utils.add_inclusive_time_frame(query, table, dt_range)
