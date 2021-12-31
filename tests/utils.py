from datetime import date, timedelta
import os
import pickle

from abautomator.collector import get_df

def get_yesterday():
    return date.today() - timedelta(days=2)

def df_from_cache(file_name, query, conn):
    try:
        result = pickle.load(
            open(get_cache_path(file_name), "rb" )
        )
    except FileNotFoundError:
        result =  get_df.get_df_from_query(query, conn)
        pickle.dump(
            result, open(get_cache_path(file_name), "wb" )
        )
    return result

def get_cache_path(file_name):
    return os.path.join("tests", "cache", f"{file_name}.p")