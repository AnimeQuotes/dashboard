from datetime import datetime

from babel.dates import format_datetime, format_timedelta


def filter_format_timedelta(dt: datetime) -> str:
    if dt is None:
        return "Unknown"

    return format_timedelta(dt - datetime.utcnow(), locale="en", add_direction=True)


def filter_format_datetime(dt: datetime) -> str:
    if dt is None:
        return "Unknown"

    return format_datetime(dt, locale="en")
