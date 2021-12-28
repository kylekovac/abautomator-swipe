from datetime import date, timedelta
import os
import pickle

from abautomator import get_df

def _get_yesterday():
    return date.today() - timedelta(days=2)

def _df_from_cache(name, query, conn):
    try:
        result = pickle.load(
            open(os.path.join("tests", f"{name}.p"), "rb" )
        )
    except FileNotFoundError:
        result =  get_df.get_df_from_query(query, conn)
        pickle.dump(
            result, open(os.path.join("tests", f"{name}.p"), "wb" )
        )
    return result