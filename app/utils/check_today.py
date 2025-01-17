from datetime import datetime


def check_date_is_today(dt: datetime) -> bool:
    """Check if provided datetime is today.

    Args:
        dt (datetime): Datetime to check

    Returns:
        bool: True if dt is today, False if not
    """

    return dt.date() == datetime.now().date()
