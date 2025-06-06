"""Provide date-related functions."""

from datetime import date, datetime
from typing import Protocol

import pytz


class SimpleTimezone(Protocol):
    """Help out the type checker."""

    def localize(self, a_date: datetime) -> datetime:
        ...  # pragma: no cover


def todays_date() -> str:
    """Provide today's date in ISO-8601 format."""

    return iso_8601(today())


def current_year() -> int:
    """Provide the current year."""

    return today().year


def today() -> date:
    """Provide today's date in the given timezone."""

    # TODO: Refactor the timezone to a config setting.
    #       But the Scrapy settings don't seem to be
    #       available in this context.
    #       See https://doc.scrapy.org/en/latest/topics/settings.html.
    tz = pytz.timezone("US/Mountain")

    return tz.localize(datetime.now()).date()


def iso_8601(a_date: date) -> str:
    """Convert the date to ISO-8601 format."""

    ISO_8601_FORMAT = "%Y-%m-%d"
    return a_date.strftime(ISO_8601_FORMAT)
