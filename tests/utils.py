from datetime import date, timedelta
import os
import pickle

from abautomator import get_query

def _get_yesterday():
    return date.today() - timedelta(days=2)

def _df_from_cache(name, query, conn):
    try:
        result = pickle.load(
            open(os.path.join("tests", f"{name}.p"), "rb" )
        )
    except FileNotFoundError:
        result =  get_query._get_query_df(query, conn)
        pickle.dump(
            result, open(os.path.join("tests", f"{name}.p"), "wb" )
        )
    return result