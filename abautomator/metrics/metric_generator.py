"""Takes a list of Naive metrics and generates segmented/nonsegmented base metrics"""
from dataclasses import dataclass
from typing import List

import sqlalchemy
from sqlalchemy import distinct
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from abautomator import metrics, utils


@dataclass
class GroupGetter():
    table_name: str
    segment_col: str

    def _get_segment_query(self, engine, dt_range):
        table = Table(
            f'echelon.{self.table_name}',
            MetaData(bind=engine),
            autoload=True,
        )

        result = select(
            getattr(table.c, self.segment_col),
            func.count().label("count"),
        ).group_by(
            getattr(table.c, self.segment_col)
        )
        result = self.add_where_clause(result, table, dt_range)

        return result

    def add_where_clause(self, query, table, dt_range):
        """ To be overridden as needed in child classes """
        return utils.add_inclusive_time_frame(query, table, dt_range) 
    
    def get_segments(self, engine, conn, dt_range):
        result_df =  utils.get_df_from_query(
            self._get_segment_query(engine, dt_range), conn
        )
        print(result_df)
        result_df = result_df[result_df["count"] > 300]  # TODO make logic less arbitrary

        return result_df[self.segment_col].tolist()


@dataclass
class GroupInfo:
    name: str                            # Human-readable name
    table_name: str                      # Where event that the metric is to be derived from lives
    table_col: str                       # Where event that the metric is to be derived from lives
    segment_col: str = None


@dataclass
class GroupMetricGenerator:
    engine: sqlalchemy.engine.Engine
    conn: sqlalchemy.engine.Connection
    dt_range: utils.DateRange
    segment_info: GroupInfo
    segment_getter: GroupGetter = None

    def __post_init__(self):
        self.segment_getter = GroupGetter(self.segment_info.table_name, self.segment_info.segment_col)

    def generate(self):
        result = []
        for segment in self.segment_getter.get_segments(self.engine, self.conn, self.dt_range):
            result.append(
                metrics.GroupMetric(
                    name=self._get_seg_full_name(segment),
                    table_name=self.segment_info.table_name,
                    table_col=self.segment_info.table_col,
                    segment_col=self.segment_info.segment_col,
                    segment_value=segment
                )
            )

        return result
    
    def _get_seg_full_name(self, segment):
        return f"{self.segment_info.name}\n({segment})"
    
    def get_segments(self, segmented_metric):
        pass
