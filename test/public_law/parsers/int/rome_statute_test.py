import pytest
import urllib

from tika import parser

from public_law.parsers.int.rome_statute import tika_pdf


class TestRomeStatute:
    def test_can_use_the_tika_api(self):
        french_xml = tika_pdf("https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf")
        assert set(french_xml.keys()) == {"metadata", "content", "status"}

    def test_raises_error_when_pdf_not_found(self):
        with pytest.raises(urllib.error.HTTPError):
            tika_pdf("https://www.icc-cpi.int/Publications/abcdefg.pdf")
