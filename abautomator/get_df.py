import pandas as pd

def get_df_from_query(query, conn):
  result = pd.read_sql(query, conn)
  result['echelon_user_id'] = result['echelon_user_id'].astype("string")
  return result

def get_user_metrics_df(users_df, metrics):
  result = users_df
  for metric_df in metrics:
    result = result.merge(metric_df, on="echelon_user_id", how="left")
  
  result = _fill_nan_metrics_with_zeros(result)

  return result

def _fill_nan_metrics_with_zeros(df):
  for col in df.columns:
    if col not in ["echelon_user_id", "exp_cond"]:
      df[col] = df[col].fillna(0)
  return df