import pytest
from urllib import error
from typing import Final


from public_law.parsers.int.rome_statute import tika_pdf, metadata, modified_at, title

FRENCH_URL: Final[str] = "https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf"


class TestRomeStatute:
    def test_can_use_the_tika_api(self):
        french_xml = tika_pdf(FRENCH_URL)

        assert set(french_xml.keys()) == {"metadata", "content", "status"}

    def test_raises_error_when_pdf_not_found(self):
        with pytest.raises(error.HTTPError):
            tika_pdf("https://www.icc-cpi.int/Publications/abcdefg.pdf")


class TestMetadata:
    def test_gets_the_title(self):
        title = metadata(FRENCH_URL)["dc:title"]

        assert title == "Statut de Rome de la Cour pénale internationale"


class TestTitle:
    def test_works_correctly(self):
        assert title(FRENCH_URL) == "Statut de Rome de la Cour pénale internationale"


class TestModifiedAt:
    def test_works_correctly(self):
        assert modified_at(FRENCH_URL) == "2021-11-02T15:46:45Z"
