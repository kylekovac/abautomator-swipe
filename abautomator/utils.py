from datetime import date, timedelta
from dataclasses import dataclass
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
import pandas as pd

@dataclass
class DateRange:
  start: date
  end: date = None

def add_inclusive_time_frame(
        query: Selectable, table: Table, dt_range: DateRange, date_col="event_date",
    ):
    if dt_range.start:
        query = query.where(
            getattr(table.c, date_col) >= dt_range.start
        )
    if dt_range.end:
        query = query.where(
            getattr(table.c, date_col) <= dt_range.end
        )
    return query

def get_df_from_query(query, conn):
    result = pd.read_sql(query, conn)
    if 'echelon_user_id' in result.columns:  # Not present in GroupGetter logic
        result['echelon_user_id'] = result['echelon_user_id'].astype("string")
    return result
