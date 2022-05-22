from typing import Protocol

from datetime import datetime, date
import pytz


class SimpleTimezone(Protocol):
    def localize(self, a_date: datetime) -> date:
        ...  # pragma: no cover


def todays_date() -> str:
    """Provide today's date in ISO-8601 format."""
    
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")
    fmt = "%Y-%m-%d"
    return mountain.localize(datetime.now()).strftime(fmt)
