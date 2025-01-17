from datetime import datetime, timedelta


def get_date_days_ago(days: int) -> datetime:
    """Get datetime for provided number of days ago from current datetime.

    Args:
        days (int): Number of days

    Returns:
        datetime: Datetime object
    """

    return datetime.now() - timedelta(days=days)
