from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable

from abautomator.metrics import BaseMetric
from abautomator import utils

@dataclass
class OnboardingBaseMetric(BaseMetric):
    name: str = None
    table_name: str = "dim_user_onboardings"
    table_col: str = None

@dataclass
class ViewedOnboardingCarouselMetric(OnboardingBaseMetric):
    name: str = "viewed_onboarding_carousel"
    table_col: str = "viewed_onboarding_carousel"

    # TODO test case for this


@dataclass
class GrantedContactsMetric(BaseMetric):
    name: str = "granted_contacts"
    table_name: str = "dim_user_onboardings"
    table_col: str = "echelon_user_id"

    def add_where_clause(self, query: Selectable, table: Table, dt_range: utils.DateRange):
        query = utils.add_inclusive_time_frame(query, table, dt_range)
        return query.where(
            table.c.completed_contacts_preprompt_permission == "granted"
        )
