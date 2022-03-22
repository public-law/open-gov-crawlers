import pytest
from urllib import error
import vcr

from public_law.parsers.int.rome_statute import (
    articles,
    language,
    metadata,
    modified_at,
    parts,
    tika_pdf,
    title,
)

ENGLISH_URL = "https://www.icc-cpi.int/Publications/Rome-Statute.pdf"
FRENCH_URL = "https://www.icc-cpi.int/Publications/Statut-de-Rome.pdf"

with open("test/fixtures/Rome-Statute.html", "r") as f:
    ENGLISH_HTML = f.read()


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


#
# Tests for finishing parsing of Rome Statute (English)
#
# Remove the @pytest.mark.skip() lines to enable the tests.
# They can be used as a todo list by enabling them one by one.
#


class TestArticles:
    """Test the articles() function."""

    @pytest.mark.skip()
    def test_returns_the_correct_amount_of_items(self):
        count = len(articles(ENGLISH_HTML))
        assert count == 131

    @pytest.mark.skip()
    def test_gets_correct_number_a(self):
        first_article = articles(ENGLISH_HTML)[0]
        assert first_article.number == "1"

    @pytest.mark.skip()
    def test_gets_correct_number_b(self):
        last_article = articles(ENGLISH_HTML).pop()
        assert last_article.number == "128"

    @pytest.mark.skip()
    def test_correctly_parses_a_complex_number(self):
        article_8_bis = articles(ENGLISH_HTML)[8]
        assert article_8_bis.number == "8 bis"

    @pytest.mark.skip()
    def test_gets_correct_part_number_a(self):
        first_article = articles(ENGLISH_HTML)[0]
        assert first_article.part_number == 1

    @pytest.mark.skip()
    def test_gets_correct_part_number_b(self):
        last_article = articles(ENGLISH_HTML).pop()
        assert last_article.part_number == 13

    @pytest.mark.skip()
    def test_gets_the_first_name(self):
        first_article = articles(ENGLISH_HTML)[0]
        assert first_article.name == "The Court"

    @pytest.mark.skip()
    def test_gets_the_last_name(self):
        last_article = articles(ENGLISH_HTML).pop()
        assert last_article.name == "Authentic Texts"

    @pytest.mark.skip()
    def test_handles_a_long_name(self):
        article_19 = articles(ENGLISH_HTML)[21]
        assert (
            article_19.name
            == "Challenges to the jurisdiction of the Court or the admissibility of the case"
        )

    @pytest.mark.skip()
    def test_unnamed_articles_should_have_empty_name_string(self):
        article_10 = articles(ENGLISH_HTML)[12]
        assert article_10.name == ""

    @pytest.mark.skip()
    def test_gets_simple_text(self):
        ...

    @pytest.mark.skip()
    def test_gets_complex_text(self):
        ...
