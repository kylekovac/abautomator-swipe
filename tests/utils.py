from datetime import date, timedelta
import os
import dill as pickle

from abautomator import utils


def get_yesterday():    
    return date.today() - timedelta(days=3)

def df_from_cache(file_name, query, conn):
    try:
        result = pickle.load(
            open(get_cache_path(file_name), "rb" )
        )
    except FileNotFoundError:
        result =  utils.get_df_from_query(query, conn)
        cache_obj(result, file_name)
    return result

def cache_obj(obj, cache_name):
    pickle.dump(
        obj, open(get_cache_path(cache_name), "wb" )
    )

def get_cache_path(file_name):
    return os.path.join("tests", "cache", f"{file_name}.p")