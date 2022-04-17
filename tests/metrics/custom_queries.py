
IOS_HS_ONE_QUERY = """
with cohort_timings as (
    select echelon_user_id, context_traits_homescreen_v_1_001, min(event_datetime) as first_, max(event_datetime) as last_
    from `citizen-ops-21adfa65.echelon.segment_app_open_2`
    where
        event_date >= PARSE_DATE('%m/%d/%Y',  '2/26/2022')
        and event_date <= PARSE_DATE('%m/%d/%Y',  '3/23/2022')
        and context_traits_homescreen_v_1_001 in ('iOSHomescreenCtrl02092022', 'iOSHomescreenTx02092022')
    group by 1, 2
)
select distinct
    a.echelon_user_id,
    case
        when a.context_traits_homescreen_v_1_001 = 'iOSHomescreenCtrl02092022' 
            and b.context_traits_homescreen_v_1_001 = 'iOSHomescreenTx02092022'
            and a.last_ <= b.first_
            then b.context_traits_homescreen_v_1_001
        else a.context_traits_homescreen_v_1_001
    end as exp_cond,
    case
        when a.context_traits_homescreen_v_1_001 = 'iOSHomescreenCtrl02092022' 
            and b.context_traits_homescreen_v_1_001 = 'iOSHomescreenTx02092022'
            and a.last_ <= b.first_
            then b.first_
        else a.first_
    end as first_event_datetime
from cohort_timings a
left join cohort_timings b
    on a.echelon_user_id = b.echelon_user_id
    and a.context_traits_homescreen_v_1_001 <> b.context_traits_homescreen_v_1_001
"""

ANDROID_HS_ONE_QUERY = """
with cohort_timings as (
    select echelon_user_id, context_traits_homescreen_v_1_001, min(event_datetime) as first_, max(event_datetime) as last_
    from `citizen-ops-21adfa65.echelon.segment_app_open_2`
    where
        event_date >= PARSE_DATE('%m/%d/%Y',  '2/26/2022')
        and event_date <= PARSE_DATE('%m/%d/%Y',  '3/23/2022')
        and context_traits_homescreen_v_1_001 in ('AndroidHomescreenCtrl02112022', 'AndroidHomescreenTx02112022')
    group by 1, 2
)
select distinct
    a.echelon_user_id,
    case
        when a.context_traits_homescreen_v_1_001 = 'AndroidHomescreenCtrl02112022' 
            and b.context_traits_homescreen_v_1_001 = 'AndroidHomescreenTx02112022'
            and a.last_ <= b.first_
            then b.context_traits_homescreen_v_1_001
        else a.context_traits_homescreen_v_1_001
    end as exp_cond,
    case
        when a.context_traits_homescreen_v_1_001 = 'AndroidHomescreenCtrl02112022' 
            and b.context_traits_homescreen_v_1_001 = 'AndroidHomescreenTx02112022'
            and a.last_ <= b.first_
            then b.first_
        else a.first_
    end as first_event_datetime
from cohort_timings a
left join cohort_timings b
    on a.echelon_user_id = b.echelon_user_id
    and a.context_traits_homescreen_v_1_001 <> b.context_traits_homescreen_v_1_001
"""
