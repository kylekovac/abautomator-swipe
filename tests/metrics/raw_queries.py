""" Raw queries for doing count comparisons w/ sqlalchemy queries """

RAW_QUERIES = {
    "friend_invites": """SELECT
        echelon_user_id
    FROM
        echelon.fct_share_completes_installs
    WHERE
        event_date >= '{start_dt}'
        and general_type = 'Invite'
    GROUP BY 1""",

    "incident_shares": """SELECT
        echelon_user_id
    FROM
        echelon.fct_share_completes_installs
    WHERE
        event_date >= '{start_dt}'
        and general_type = 'Incident Shares'
    GROUP BY 1""",

    "user_sessions": """SELECT
      echelon_user_id
    FROM
      echelon.fct_user_sessions
    WHERE
      event_date >= '{start_dt}'
    GROUP BY 1""",

    "incident_views": """SELECT
      echelon_user_id
    FROM
      echelon.fct_incident_views
    WHERE
      event_date >= '{start_dt}'
    GROUP BY 1""",

    "trial_starts": """SELECT
      echelon_user_id
    FROM
      echelon.dim_purchased_subscriptions
    WHERE
      event_date >= '{start_dt}'
      and transaction_id = original_transaction_id
    GROUP BY 1""",
}