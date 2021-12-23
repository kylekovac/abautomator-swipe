
from sqlalchemy import create_engine

from abautomator import main

def test_answer():
    engine = create_engine(f'bigquery://{main.GCP_PROJECT_ID}')
    conn = engine.connect()
    users = main.get_users(engine, main.exp_config)

    print(users)

    # result = conn.execute(users).all()
    # print(len(result))
    # print(result[0:10])
    
    assert True