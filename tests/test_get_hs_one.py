import pytest
from datetime import date

from abautomator import describer, metrics, collector, metrics, analyzer
from abautomator.utils import DateRange
from tests import utils

CUSTOM_QUERIES = {
    "ios": """
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
    """,
    "android": """
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
}

@pytest.mark.build
def test_get_homescreen_one_anal_ios(engine):

    print("collecting data")
    coll = collector.Collector(
        engine=engine,
        conds=[
            'iOSHomescreenCtrl02092022',
            'iOSHomescreenTx02092022',
        ],
        metrics=[
            metrics.METRIC_LOOKUP["incident_share_completes"],
            metrics.METRIC_LOOKUP["incident_views"],
            metrics.METRIC_LOOKUP["all_sessions"],
            metrics.METRIC_LOOKUP["organic_sessions"],
            metrics.METRIC_LOOKUP["push_driven_sessions"],
        ],
        event='segment_app_open_2',
        event_prop='context_traits_homescreen_v_1_001',
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=CUSTOM_QUERIES['ios'],
    )
    coll.collect_data()

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="iOSHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        # ctrl_name=self.ctrl_name.replace(self.name, ""),
        ctrl_name='Ctrl02092022',
    )

    utils.cache_obj(analy, f"homescreen_analy_ios")

@pytest.mark.build
def test_get_homescreen_one_anal_android(engine):

    print("collecting data")
    coll = collector.Collector(
        engine=engine,
        conds=[
            'AndroidHomescreenCtrl02112022',
            'AndroidHomescreenTx02112022',
        ],
        metrics=[
            metrics.METRIC_LOOKUP["incident_views"],
            metrics.METRIC_LOOKUP["incident_share_completes"],
            metrics.METRIC_LOOKUP["incident_share_attempts"],
            # metrics.METRIC_LOOKUP["all_sessions"],
            # metrics.METRIC_LOOKUP["organic_sessions"],
            # metrics.METRIC_LOOKUP["push_driven_sessions"],
        ],
        event='segment_app_open_2',
        event_prop='context_traits_homescreen_v_1_001',
        dt_range=DateRange(date(2022, 2, 26), date(2022, 3, 23)),
        custom_users_query=CUSTOM_QUERIES['android'],
    )
    coll.collect_data()

    print("describing data")
    # init and run the describer
    desc = describer.Describer(
        metrics=coll.metrics
    )
    outcomes_dict = desc.describe_data(exp_name="AndroidHomescreen")

    print("analyzing data")
    analy =  analyzer.Analyzer(
        outcomes=outcomes_dict,
        # ctrl_name=self.ctrl_name.replace(self.name, ""),
        ctrl_name='Ctrl02112022',
    )

    utils.cache_obj(analy, f"homescreen_analy_android")
