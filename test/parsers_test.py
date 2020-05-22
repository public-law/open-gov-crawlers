import pytest
from scrapy.selector import Selector
from typing import Any, IO

from oar.parsers import meta_sections, parse_division, statute_meta


def fixture(filename: str) -> IO[Any]:
    return open(f"test/fixtures/{filename}")


@pytest.mark.describe("statute_meta()")
class TestStatuteMeta:
    def test_a_single_chapter_citation(self):
        raw_text = "ORS 183"
        expected = ["ORS 183"]
        assert statute_meta(raw_text) == expected

    def test_the_ampersand_separator(self):
        raw_text = "ORS 181A.235 &amp; ORS 192"
        expected = ["ORS 181A.235", "ORS 192"]
        assert statute_meta(raw_text) == expected

    def test_parses_a_range_as_a_single_item(self):
        raw_text = "ORS 243.061 - 243.302"
        expected = ["ORS 243.061 - 243.302"]
        assert statute_meta(raw_text) == expected

    def test_a_mix_of_ranges_and_single_cites(self):
        raw_text = "ORS 183.310 - 183.550, 192.660, 243.061 - 243.302 &amp; 292.05"
        expected = ["ORS 183.310 - 183.550",
                    "192.660", "243.061 - 243.302", "292.05"]
        assert statute_meta(raw_text) == expected

    def test_citations_to_the_OR_constitution(self):
        raw_text = "ORS 273.045, 273.775 - 273.79 &amp; OR Const., Art. VIII &amp; Sec. 5"
        expected = ["ORS 273.045", "273.775 - 273.79",
                    "OR Const., Art. VIII", "Sec. 5"]
        assert statute_meta(raw_text) == expected

    def test_const_cite_without_comma(self):
        raw_text = "ORS 407.115, 407.125 &amp; Art. XI-A OR Const."
        expected = ["ORS 407.115", "407.125", "Art. XI-A OR Const."]
        assert statute_meta(raw_text) == expected

    def test_const_cite_with_comma_after_article(self):
        raw_text = "OR Const. Art. XV, Sec. 4(4) &amp; ORS 461"
        expected = ["OR Const. Art. XV, Sec. 4(4)", "ORS 461"]
        assert statute_meta(raw_text) == expected


@pytest.mark.describe("meta_sections()")
class TestMetaSections:
    def test_parses_when_all_three_types_are_present(self):
        raw_text = "<p><b>Statutory/Other Authority:</b> ORS 243.061 - 243.302<br><b>Statutes/Other Implemented:</b> ORS.243.125(1)<br><b>History:</b><br>PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03<br> </p>"
        expected = {
            "authority": ["ORS 243.061 - 243.302"],
            "implements": ["ORS.243.125(1)"],
            "history": "PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03",
        }
        assert meta_sections(raw_text) == expected


@pytest.mark.describe("fixture()")
class TestFixture:
    def test_can_access_a_fixture(self):
        with fixture('division_450.html') as f:
            html = f.read()
            assert len(html) > 0


@pytest.mark.describe('parse_division()')
class TestParseDivision:

    def test_number_of_rules(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            assert len(parse_division(html)) == 2

    def test_rule_numbers(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            numbers = [n['number'] for n in parse_division(html)]
            assert numbers == ['123-450-0000', '123-450-0010']

    def test_rule_names(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            names = [n['name'] for n in parse_division(html)]

            assert names == ['Definitions', 'Grants']

    def test_rule_text(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            expected_text = "<p>(1) “Commission” means the Oregon Arts Commission.</p>\n<p>(2) “Executive Director” means the administrator of the Arts Program of the Oregon Business Development Department.</p>"
            first_text = parse_division(html)[0]['text']

            assert first_text == expected_text

    def test_rule_authority(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            expected = ['ORS 359']
            first_authority = parse_division(html)[0]['authority']

            assert first_authority == expected

    def test_rule_implements(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            expected = ['ORS 359']
            first_implements = parse_division(html)[0]['implements']

            assert first_implements == expected

    def test_rule_history(self):
        with fixture('division_450.html') as f:
            html = Selector(text=f.read())
            expected = 'OBDD 2-2011, f. &amp; cert. ef. 1-3-11'
            first_history = parse_division(html)[0]['history']

            assert first_history == expected
