from dataclasses import dataclass
from sqlalchemy import and_, distinct
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.selectable import Selectable
from sqlalchemy.sql import func, select, text
from sqlalchemy import and_, case

from abautomator.metrics import BaseMetric
from abautomator import utils, config

@dataclass
class SignupActicationMetric(BaseMetric):
    name: str = "signup_activation"
    table_name: str = "fct_user_signups"
    table_col: str = "id"

    def _get_metric_query(self, engine, dt_range):

        signups = Table(
            f'{config.GCP_DATASET}.fct_user_signups',
            MetaData(bind=engine),
            autoload=True,
        )

        incident_views = Table(
            f'{config.GCP_DATASET}.fct_incident_views',
            MetaData(bind=engine),
            autoload=True,
        )

        query = select(
            signups.c.echelon_user_id,
            case(
                (func.count(distinct(incident_views.c.id)) > 3, 1),
                else_=0,
                ).label(self.n_label),  # TODO: think about removing this
            case(
                (func.count(distinct(incident_views.c.id)) > 3, 1),
                else_=0,
                ).label(self.pct_label),
        ).select_from(
            signups.outerjoin(
                incident_views,
                and_(
                    signups.c.echelon_user_id == incident_views.c.echelon_user_id,
                    func.date_diff(
                        incident_views.c.event_datetime, signups.c.join_date,
                        text('MINUTE'),
                    ) <= 1440,
                    func.date_diff(
                        incident_views.c.event_datetime, signups.c.join_date,
                        text('MINUTE'),
                    ) >= 0,
                ),
                # isouter=True,
            )
        ).group_by(
            signups.c.echelon_user_id,
        )

        return utils.add_inclusive_time_frame(
            query, signups, dt_range, date_col="join_date",
        )
