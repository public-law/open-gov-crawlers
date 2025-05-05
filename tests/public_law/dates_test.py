import re
from subprocess import check_output

from public_law.dates import todays_date


class TestTodaysDate:
    def test_is_in_iso_8601_format(self):
        assert re.match(r"^\d\d\d\d-\d\d-\d\d$", todays_date())

    def test_matches_unix_date_cmd(self):
        unix_date = check_output(["date", "+%Y-%m-%d"], encoding="utf8").strip()
        assert todays_date() == unix_date
