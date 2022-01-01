from datetime import date
from sqlalchemy.schema import Table
from sqlalchemy.sql.selectable import Selectable
import pandas as pd

def add_time_frame(query: Selectable, table: Table, start_dt: date = None, end_dt: date = None):
  if start_dt:
    query = query.where(
      table.c.event_date >= start_dt
    )
  if end_dt:
    query = query.where(
      table.c.event_date <= end_dt
    )
  return query

def get_df_from_query(query, conn):
  result = pd.read_sql(query, conn)
  result['echelon_user_id'] = result['echelon_user_id'].astype("string")
  return result