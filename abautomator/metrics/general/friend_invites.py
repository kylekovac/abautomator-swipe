from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric

@dataclass
class FriendInvitesMetric(BaseMetric):
    name: str = "Friend Invites"
    table_name: str = "fct_share_completes_installs"
    table_col: str = "id"

    def add_where_clause(self, query: Selectable, table: Table):
        return query.where(
            table.c.general_type == "Invite"
        )
