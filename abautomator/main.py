from datetime import date

from google.cloud import bigquery
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import func, select

exp_config = {
  "EXP_START": date(2021, 12, 10),
  "EXP_END": None,
  "DEVICES": ["android", "ios"],
  "COHORTING_PROP": "context_traits_onboarding_flow_001",
  "COHORTING_TABLE": "segment_signup_flow_started",
  "COHORT_NAMES": [
    'Dec1021InspirationMomentFinalVideo01',
    'Dec1021InspirationMomentFinalVideo02',
    'Dec1021InspirationMomentFinalCarousel01',
    'Dec1021InspirationMomentFinalCarousel02',
    'Dec1021InspirationMomentFinalCarousel03',
    'Dec1021InspirationMomentFinalCarousel04',
    'Dec1021InspirationMomentFinalControl',
  ],
}

GCP_PROJECT_ID = 'citizen-ops-21adfa65' # Prod

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
