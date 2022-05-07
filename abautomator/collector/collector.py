""" Collects experiment data from BigQuery"""
from datetime import date
from dataclasses import dataclass, field
from typing import List

import pandas as pd
import sqlalchemy
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import case


from abautomator import metrics, utils, config


@dataclass
class Collector:
    engine: sqlalchemy.engine.Engine
    conds: List[str]                  # column values
    metrics: List[metrics.BaseMetric] # Naive Metric wrapper
    event: str                        # table/thing user does to become exp participant
    event_prop: str                   # table col with exp_cond info
    dt_range: utils.DateRange
    custom_users_query: str=None
    users_df: pd.DataFrame=None


    def collect_data(self) -> None:
        with self.engine.connect() as conn:
            self._populate_users_df(conn)
            self._populate_metric_data_dfs(conn)
    
    def _populate_users_df(self, conn):
        if self.users_df is None:
            self.users_df = utils.get_df_from_query(
                self.custom_users_query or self._get_users_query(), conn,
            )

    def _get_users_query(self):
        event = Table(
            f'{config.GCP_DATASET}.{self.event}',
            MetaData(bind=self.engine),\
            autoload=True
        )
        signups = Table(
            f'{config.GCP_DATASET}.fct_user_signups',
            MetaData(bind=self.engine),
            autoload=True,
        )

        result = select(
            event.c.echelon_user_id,
            event.c.device_type,
            getattr(event.c, self.event_prop).label("exp_cond"),
            case(
                [(signups.c.join_date >= self.dt_range.start, "new")],
                else_= "existing"
            ).label("user_type"),
        ).select_from(
            event.outerjoin(
                signups,
                event.c.echelon_user_id == signups.c.echelon_user_id
            )
        ).where(
            getattr(event.c, self.event_prop).in_(self.conds)
        ).distinct()
        # Ommitting first_event_datetime for now

        result = utils.add_inclusive_time_frame(result, event, self.dt_range)
        return result
    
    def _populate_metric_data_dfs(self, conn):
        for metric in self.metrics:
            metric.populate_user_metric_df(self, conn)  # Ideal state
