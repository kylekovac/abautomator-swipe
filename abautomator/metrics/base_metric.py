from dataclasses import dataclass
import pandas as pd
import sqlalchemy
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from abautomator import utils
# from abautomator.metrics import metric_lookup

@dataclass
class MetricInfo:
    name: str                            # Human-readable name
    table_name: str                      # Where event that the metric is to be derived from lives
    table_col: str                       # Where event that the metric is to be derived from lives

@dataclass
class BaseMetric(MetricInfo):
    user_metric_df: pd.DataFrame = None  # To be populated. Per user exp_cond + metric quantity data

    def __post_init__(self):
        self.n_label = f"n_{self._cleaned_name()}"
        self.pct_label = f"pct_{self._cleaned_name()}"
        # assert self.name in metric_lookup.METRIC_LOOKUP.keys(), "Invalid Metric"
    
    def _cleaned_name(self):
        return self._clean(self.name)
    
    def _clean(self, str_):
         return str_.lower().replace(' ', '_')
    
    def populate_user_metric_df(self, coll, conn):
        metric_df = self._get_metric_df(coll.engine, conn, coll.dt_range)
        self.user_metric_df = self._add_exp_cond_to_metric(coll.users_df, metric_df)
    
    def _get_metric_df(self, engine, conn, dt_range):
        return utils.get_df_from_query(
            self._get_metric_query(engine, dt_range), conn
        )

    def _get_metric_query(self, engine, dt_range):
        table = Table(
            f'echelon.{self.table_name}',
            MetaData(bind=engine),
            autoload=True,
        )

        result = select(
            table.c.echelon_user_id,
            func.count(getattr(table.c, self.table_col)).label(self.n_label),
            sqlalchemy.case(
                (
                    func.count(getattr(table.c, self.table_col)) > 0, 1
                ),
                else_=0
            ).label(self.pct_label),
        ).group_by(
            table.c.echelon_user_id,
        )
        result = self.add_where_clause(result, table, dt_range)

        return result

    def add_where_clause(self, query, table, dt_range):
        """ To be overridden as needed in child classes """
        return utils.add_inclusive_time_frame(query, table, dt_range)
    
    def _add_exp_cond_to_metric(self, users_df, metric_df):

        result = users_df.copy()
        result = result.merge(metric_df, on="echelon_user_id", how="left")
    
        result = _fill_nan_metrics_with_zeros(result)

        return result

def _fill_nan_metrics_with_zeros(df):
  for col in df.columns:
    if col not in ["echelon_user_id", "exp_cond"]:
      df[col] = df[col].fillna(0)
  return df
