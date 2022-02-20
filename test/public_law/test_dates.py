import re

from public_law.dates import todays_date


class TestTodaysDate:
    def test_is_in_iso_8601_format(self):
        assert re.match(r"^\d\d\d\d-\d\d-\d\d$", todays_date())
