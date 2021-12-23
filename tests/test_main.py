from datetime import date, timedelta
from sqlalchemy import create_engine

from abautomator import main


def test_answer():
    engine = create_engine(f'bigquery://{main.GCP_PROJECT_ID}')
    test_config = main.exp_config
    test_config["EXP_START"] = date.today() - timedelta(days = 1)
    users = main.get_users(engine, test_config)

    print(users)

    conn = engine.connect()
    result = conn.execute(users).all()
    print(len(result))

    assert len(result) > 1    
