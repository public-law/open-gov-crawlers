from typing import Protocol

from datetime import datetime, date
import pytz


class SimpleTimezone(Protocol):
    def localize(self, a_date: datetime) -> date:
        ...  # pragma: no cover


def todays_date() -> str:
    """Provide today's date in ISO-8601 format."""

    return iso_8601(today())


def today() -> date:
    """Provide today's date in the given timezone."""

    # TODO: Refactor the timezone to a config setting.
    #       But the Scrapy settings don't seem to be
    #       available in this context.
    #       See https://doc.scrapy.org/en/latest/topics/settings.html.
    mountain: SimpleTimezone = pytz.timezone("US/Mountain")  # type: ignore
    return mountain.localize(datetime.now())


def iso_8601(a_date: date) -> str:
    """Convert the date to ISO-8601 format."""

    ISO_8601_FORMAT = "%Y-%m-%d"
    return a_date.strftime(ISO_8601_FORMAT)
