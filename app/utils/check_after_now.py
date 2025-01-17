from datetime import datetime


def check_after_now(dt: datetime) -> bool:
    """Check if provided datetime is after now.

    Args:
        dt (datetime): Datetime to check

    Returns:
        bool: True if dt is after now, False if not
    """

    return dt >= datetime.now()
