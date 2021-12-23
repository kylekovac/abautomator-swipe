from datetime import date
from dataclasses import dataclass

from google.cloud import bigquery
from sqlalchemy.engine import *
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

from abautomator.config import GCP_PROJECT_ID



from typing import List

@dataclass
class Cohort:
  control: str
  treatment_groups: List[str]
  event: str
  event_property: str


@dataclass
class Experiment:
  cohort: Cohort
  start: date
  end: date=None
  devices: List[str]=["android", "ios"]


def get_users(engine, exp_config):
  table = Table(f'echelon.{exp_config["COHORTING_TABLE"]}', MetaData(bind=engine), autoload=True)

  result = select(
      table.c.echelon_user_id, 
      getattr(table.c, exp_config["COHORTING_PROP"]).label("cohort"),
  ).where(
      getattr(table.c, exp_config["COHORTING_PROP"]).in_(exp_config["COHORT_NAMES"])
  ).group_by(
      table.c.echelon_user_id, 
      getattr(table.c, exp_config["COHORTING_PROP"]),
  )

  # Ommitting first_event_datetime for now

  result = add_time_frame(result, table, exp_config)

  return result

def add_time_frame(query, table, exp_config):
  if exp_config["EXP_START"]:
    query = query.where(
      table.c.event_date >= exp_config["EXP_START"]
    )
  if exp_config["EXP_END"]:
    query = query.where(
      table.c.event_date <= exp_config["EXP_END"]
    )
  return query

class Event:
  def __init__(self, table_name, col):
    self.table_name = table_name
    self.col = col

class EventMetric:
  def __init__(self, event, exp_config):
    self.event = event
    self.exp_config = exp_config
  
  def get_query(self, conn):
    table = Table(f'echelon.{self.event.table_name}', MetaData(bind=engine), autoload=True)

    result = select(
        table.c.echelon_user_id,
        func.count(getattr(table.c, self.event.col).distinct()).label("n_events")
    ).group_by(
        table.c.echelon_user_id,
    )
    result = add_time_frame(result, table, self.exp_config)

    return result
