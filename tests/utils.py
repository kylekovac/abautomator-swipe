from datetime import date, timedelta

def _get_yesterday():
    return date.today() - timedelta(days=2)
