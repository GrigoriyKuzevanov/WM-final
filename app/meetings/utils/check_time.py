from datetime import datetime


def check_datetime_after_now(dt_to_check: datetime) -> bool:
    """Check datetime object if it after now.

    Args:
        dt_to_check (datetime): Datetime object to check

    Returns:
        bool: True if dt_to_check after now, False if not
    """

    return dt_to_check > datetime.now()
