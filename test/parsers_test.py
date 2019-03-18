import pytest
from oar.parsers import statute_meta


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
def test_statute_meta_constituion():
    raw_text = "ORS 273.045, 273.775 - 273.79 & OR Const., Art. VIII & Sec. 5"
    expected = ["ORS 273.045", "273.775 - 273.79", "OR Const., Art. VIII", "Sec. 5"]
    assert statute_meta(raw_text) == expected
