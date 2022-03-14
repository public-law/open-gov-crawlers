import pytest
import urllib

from tika import parser

from public_law.parsers.int.rome_statute import tika_pdf, metadata

statute_french = "https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf"


class TestRomeStatute:
    def test_can_use_the_tika_api(self):
        french_xml = tika_pdf(statute_french)
        assert set(french_xml.keys()) == {"metadata", "content", "status"}

    def test_raises_error_when_pdf_not_found(self):
        with pytest.raises(urllib.error.HTTPError):
            tika_pdf("https://www.icc-cpi.int/Publications/abcdefg.pdf")


class TestMetadata:
    def test_gets_the_title(self):
        title = metadata(statute_french)["dc:title"]

        assert title == "Statut de Rome de la Cour pénale internationale"
