import pytest
from urllib import error
import vcr

from public_law.parsers.int.rome_statute import (
    language,
    metadata,
    modified_at,
    parts,
    tika_pdf,
    title,
)

ENGLISH_URL = "https://www.icc-cpi.int/Publications/Rome-Statute.pdf"
FRENCH_URL = "https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf"


class TestTikaPdf:
    @vcr.use_cassette()  # type: ignore
    def test_can_use_the_tika_api(self):
        french_xml = tika_pdf(FRENCH_URL)

        assert set(french_xml.keys()) == {"metadata", "content", "status"}

    @vcr.use_cassette()  # type: ignore
    def test_raises_error_when_pdf_not_found(self):
        with pytest.raises(error.HTTPError):
            tika_pdf("https://www.icc-cpi.int/Publications/abcdefg.pdf")


class TestMetadata:
    @vcr.use_cassette()  # type: ignore
    def test_gets_the_title(self):
        title = metadata(FRENCH_URL)["dc:title"]

        assert title == "Statut de Rome de la Cour pénale internationale"


class TestTitle:
    @vcr.use_cassette()  # type: ignore
    def test_works_correctly(self):
        assert title(FRENCH_URL) == "Statut de Rome de la Cour pénale internationale"


class TestModifiedAt:
    @vcr.use_cassette()  # type: ignore
    def test_works_correctly(self):
        assert modified_at(FRENCH_URL) == "2021-11-02T15:46:45Z"


class TestLanguage:
    @vcr.use_cassette()  # type: ignore
    def test_detects_french(self):
        assert language(FRENCH_URL) == "fr"

    @vcr.use_cassette()  # type: ignore
    def test_detects_english(self):
        assert language(ENGLISH_URL) == "en"


class TestParts:
    @vcr.use_cassette()  # type: ignore
    def test_gets_the_name_right_1(self):
        first_name = parts(ENGLISH_URL)[0].name

        assert first_name == "Establishment of the Court"

    @vcr.use_cassette()  # type: ignore
    def test_gets_the_name_right_2(self):
        last_name = parts(ENGLISH_URL).pop().name

        assert last_name == "Final Clauses"

    @vcr.use_cassette()  # type: ignore
    def test_gets_the_correct_number_of_parts(self):
        number_returned = len(parts(ENGLISH_URL))

        assert number_returned == 13

    @vcr.use_cassette()  # type: ignore
    def test_gets_the_number_right_1(self):
        last_number = parts(ENGLISH_URL).pop().number

        assert last_number == 13
