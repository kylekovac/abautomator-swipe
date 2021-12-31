from dataclasses import dataclass
import pandas as pd

# from abautomator.collector import get_df

@dataclass
class Metric:
    name: str                     # Human-readable name
    table_name: str               # Where event that the metric is to be derived from lives
    table_col: str                # Where event that the metric is to be derived from lives
    data_df: pd.DataFrame = None  # To be populated

    def __post_init__(self):
        self.n_label = f"n_{self.name.lower().replace(' ', '_')}"
        self.pct_label = f"pct_{self.name.lower().replace(' ', '_')}"
    
    # def populate_data_df(self, coll):
    #     # metric_df = get_df.get_df_from_query(
    #     #     self._get_metric_query(metric), conn,
    #     # )
    #     pass

    
    # def _get_metric_query(self, metric: metric.Metric):
    #     table = Table(f'echelon.{metric.table_name}', MetaData(bind=self.engine), autoload=True)

    #     result = select(
    #         table.c.echelon_user_id,
    #         func.count(getattr(table.c, metric.table_col)).label(metric.n_label),
    #         sqlalchemy.case(
    #             (
    #             func.count(getattr(table.c, metric.table_col)) > 0, 1
    #             ),
    #             else_=0
    #         ).label(metric.pct_label),
    #     ).group_by(
    #         table.c.echelon_user_id,
    #     )
    #     result = utils.add_time_frame(result, table, self.start_dt, self.end_dt)

    #     return result
