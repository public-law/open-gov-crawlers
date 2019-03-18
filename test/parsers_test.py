import pytest
from oar.parsers import statute_meta, meta_sections


def test_statute_meta_1():
    raw_text = "ORS 183"
    expected = ["ORS 183"]
    assert statute_meta(raw_text) == expected


def test_statute_meta_2():
    raw_text = "ORS 181A.235 & ORS 192"
    expected = ["ORS 181A.235", "ORS 192"]
    assert statute_meta(raw_text) == expected


def test_statute_meta_3():
    raw_text = "ORS 243.061 - 243.302"
    expected = ["ORS 243.061 - 243.302"]
    assert statute_meta(raw_text) == expected


def test_statute_meta_4():
    raw_text = "ORS 183.310 - 183.550, 192.660, 243.061 - 243.302 & 292.05"
    expected = ["ORS 183.310 - 183.550", "192.660", "243.061 - 243.302", "292.05"]
    assert statute_meta(raw_text) == expected


@pytest.mark.xfail
def test_statute_meta_constitution():
    raw_text = "ORS 273.045, 273.775 - 273.79 & OR Const., Art. VIII & Sec. 5"
    expected = ["ORS 273.045", "273.775 - 273.79", "OR Const., Art. VIII", "Sec. 5"]
    assert statute_meta(raw_text) == expected


def test_meta_sections():
    raw_text = "<p><b>Statutory/Other Authority:</b> ORS 243.061 - 243.302<br><b>Statutes/Other Implemented:</b> ORS.243.125(1)<br><b>History:</b><br>PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03<br></p>"
    expected = {
        "authority": ["ORS 243.061 - 243.302"],
        "implements": ["ORS.243.125(1)"],
        "history": "PEBB 2-2005, f. 7-26-05, cert. ef. 7-29-05<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-2003, f. &amp; cert. ef. 12-4-03",
    }
    assert meta_sections(raw_text) == expected
