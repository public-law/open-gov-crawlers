from oar.parsers import statute_meta


def test_statute_meta_1():
    raw_text = "ORS 183"
    expected = ("ORS 183",)
    assert statute_meta(raw_text) == expected


def test_statute_meta_2():
    raw_text = "ORS 181A.235 & ORS 192"
    expected = ["181A.235", "ORS 192"]
    assert statute_meta(raw_text) == expected
