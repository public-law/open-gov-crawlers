import pytest
from oar.parsers import statute_meta, meta_sections


@pytest.mark.describe("statute_meta()")
class TestStatuteMeta:
    def test_handles_a_single_chapter_citation(self):
        raw_text = "ORS 183"
        expected = ["ORS 183"]
        assert statute_meta(raw_text) == expected

    def test_handles_the_ampersand_separator(self):
        raw_text = "ORS 181A.235 &amp; ORS 192"
        expected = ["ORS 181A.235", "ORS 192"]
        assert statute_meta(raw_text) == expected

    def test_parses_a_range_as_a_single_item(self):
        raw_text = "ORS 243.061 - 243.302"
        expected = ["ORS 243.061 - 243.302"]
        assert statute_meta(raw_text) == expected

    def test_handles_a_mix_of_ranges_and_single_cites(self):
        raw_text = "ORS 183.310 - 183.550, 192.660, 243.061 - 243.302 &amp; 292.05"
        expected = ["ORS 183.310 - 183.550",
                    "192.660", "243.061 - 243.302", "292.05"]
        assert statute_meta(raw_text) == expected

    def test_handles_citations_to_the_OR_constitution(self):
        raw_text = "ORS 273.045, 273.775 - 273.79 &amp; OR Const., Art. VIII &amp; Sec. 5"
        expected = ["ORS 273.045", "273.775 - 273.79",
                    "OR Const., Art. VIII", "Sec. 5"]
        assert statute_meta(raw_text) == expected

    def test_handles_const_cite_without_comma(self):
        raw_text = "ORS 407.115, 407.125 &amp; Art. XI-A OR Const."
        expected = ["ORS 407.115", "407.125", "Art. XI-A OR Const."]
        assert statute_meta(raw_text) == expected

    def test_handles_const_cite_with_comma_after_article(self):
        raw_text = "OR Const. Art. XV, Sec. 4(4) &amp; ORS 461"
        expected = ["OR Const. Art. XV, Sec. 4(4)", "ORS 461"]
        assert statute_meta(raw_text) == expected


@pytest.mark.describe("meta_sections()")
class TestMetaSections:
    def test_parses_when_all_three_types_are_present(self):
        raw_text = "<p><b>Statutory/Other Authority:</b> ORS 243.061 - 243.302<br><b>Statutes/Other Implemented:</b> ORS.243.125(1)<br><b>History:</b><br>PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03<br></p>"
        expected = {
            "authority": ["ORS 243.061 - 243.302"],
            "implements": ["ORS.243.125(1)"],
            "history": "PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03",
        }
        assert meta_sections(raw_text) == expected
