import pytest
from urllib import error

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


class TestTikaPdf:
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


class TestLanguage:
    def test_detects_french(self):
        assert language(FRENCH_URL) == "fr"

    def test_detects_english(self):
        assert language(ENGLISH_URL) == "en-US"


class TestParts:
    def test_gets_the_name_right_1(self):
        first_name = parts(ENGLISH_URL)[0].name

        assert first_name == "Establishment of the Court"

    def test_gets_the_name_right_2(self):
        last_name = parts(ENGLISH_URL).pop().name

        assert last_name == "Final Clauses"

    def test_gets_the_correct_number_of_parts(self):
        number_returned = len(parts(ENGLISH_URL))

        assert number_returned == 13

    def test_gets_the_number_right_1(self):
        last_number = parts(ENGLISH_URL).pop().number

        assert last_number == 13


#
# Tests for finishing parsing of Rome Statute (English)
#
# Remove the @pytest.mark.skip() lines to enable the tests.
# They can be used as a todo list by enabling them one by one.
#
# The HTML as given has its content divided into pages from
# the PDF. It might be very useful to remove these page divs
# like so, using Beautiful Soup:
#
#   for page_div in soup.find_all('div', class_='page'):
#     page_div.unwrap()
#


class TestArticles:
    """Test the articles() function."""

    def test_returns_the_correct_amount_of_items(self):
        count = len(articles(ENGLISH_URL))
        assert count == 131

    #
    # .number attribute
    #

    def test_gets_correct_number_a(self):
        first_article = articles(ENGLISH_URL)[0]
        assert first_article.number == "1"

    def test_gets_correct_number_b(self):
        last_article = articles(ENGLISH_URL).pop()
        assert last_article.number == "128"

    def test_correctly_parses_a_complex_number(self):
        article_8_bis = articles(ENGLISH_URL)[8]
        assert article_8_bis.number == "8 bis"

    def test_handles_numbers_with_supertext(self):
        article_5 = articles(ENGLISH_URL)[4]
        assert article_5.number == "5"

    #
    # .part_number attribute
    #

    def test_gets_correct_part_number_a(self):
        first_article = articles(ENGLISH_URL)[0]
        assert first_article.part_number == 1

    def test_gets_correct_part_number_b(self):
        last_article = articles(ENGLISH_URL).pop()
        assert last_article.part_number == 13

    #
    # .name attribute
    #

    def test_gets_the_first_name(self):
        first_article = articles(ENGLISH_URL)[0]
        assert first_article.name == "The Court"

    def test_gets_the_last_name(self):
        last_article = articles(ENGLISH_URL).pop()
        assert last_article.name == "Authentic texts"

    def test_handles_a_long_name(self):
        article_19 = articles(ENGLISH_URL)[21]
        assert (
            article_19.name
            == """Challenges to the jurisdiction of the Court or the admissibility of a case"""
        )

    def test_unnamed_articles_should_have_empty_name_string(self):
        article_10 = articles(ENGLISH_URL)[10]
        assert article_10.name == ""

    #
    # .text attribute
    #
    # Article text is expected to be flattened outlines. In other
    # words, it's up to front-end apps to display the paragraphs
    # in indented form. The reason for doing this, is we've already
    # lost the nesting information in the PDF-to-HTML conversion
    # by Tika. So this parser is only responsible for conveying the
    # flattened form found in the HTML input.
    #

    def test_gets_simple_text(self):
        article_2_text = articles(ENGLISH_URL)[1].text
        expected_text = "The Court shall be brought into relationship with the United Nations through an agreement to be approved by the Assembly of States Parties to this Statute and thereafter concluded by the President of the Court on its behalf."

        assert article_2_text == expected_text

    def test_gets_complex_text(self):
        """In this example, there are just two lines/paragraphs. Each
        begins with the outline number and has normalized internal
        whitespace."""

        article_4_text = articles(ENGLISH_URL)[3].text
        expected_text = (
            "1. The Court shall have international legal personality. It shall also have such legal capacity as may be necessary for the exercise of its functions and the fulfilment of its purposes.\n"
            "2. The Court may exercise its functions and powers, as provided in this Statute, on the territory of any State Party and, by special agreement, on the territory of any other State."
        )

        assert article_4_text == expected_text

    def test_handles_nested_outline(self):
        """This shows each paragraph from the HTML
        returned in the same, flattened form."""

        article_12_text = articles(ENGLISH_URL)[12].text  # It's the 13th Article.
        expected_text = (
            "1. A State which becomes a Party to this Statute thereby accepts the jurisdiction of the Court with respect to the crimes referred to in article 5.\n"
            "2. In the case of article 13, paragraph (a) or (c), the Court may exercise its jurisdiction if one or more of the following States are Parties to this Statute or have accepted the jurisdiction of the Court in accordance with paragraph 3:\n"
            "(a) The State on the territory of which the conduct in question occurred or, if the crime was committed on board a vessel or aircraft, the State of registration of that vessel or aircraft;\n"
            "(b) The State of which the person accused of the crime is a national.\n"
            "3. If the acceptance of a State which is not a Party to this Statute is required under paragraph 2, that State may, by declaration lodged with the Registrar, accept the exercise of jurisdiction by the Court with respect to the crime in question. The accepting State shall cooperate with the Court without any delay or exception in accordance with Part 9."
        )

        assert article_12_text == expected_text

    def test_handles_content_across_page_break(self):
        article_19_text = articles(ENGLISH_URL)[21].text.split("\n")[0:2]
        expected_lines = [
            "1. The Court shall satisfy itself that it has jurisdiction in any case brought before it. The Court may, on its own motion, determine the admissibility of a case in accordance with article 17.",
            "2. Challenges to the admissibility of a case on the grounds referred to in article 17 or challenges to the jurisdiction of the Court may be made by:"
        ]

        assert article_19_text == expected_lines

    #
    # Tests for a parser bug: some articles' name isn't picked up.
    # Instead, it's parsed as the start of the text.
    #
    # The pattern is, articles that are parsing correctly have HTML
    # like this:
    #
    # <p>Article 4
    # Legal status and powers of the Court
    # </p>
    #
    # Those that miss the name have HTML like this:
    #
    # <p>Article 51
    # </p>
    # <p>Crimes within the jurisdiction of the Court
    # </p>
    #
    # LOOK OUT: Two articles (10 and 124) are unnamed, and
    # have HTML that's similar to the broken case, e.g.:
    #
    # <p>Article 10
    # </p>
    # <p>Nothing in this Part shall be interpreted as limiting or prejudicing in any way existing or
    # developing rules of international law for purposes other than this Statute.
    # </p>

    def test_article_5_has_correct_name(self):
        article_5 = articles(ENGLISH_URL)[4]
        assert article_5.name == "Crimes within the jurisdiction of the Court"

    def test_article_5_does_not_repeat_the_name(self):
        article_5 = articles(ENGLISH_URL)[4]
        assert article_5.text.startswith("The jurisdiction of the Court shall be")

    def test_article_8_has_correct_name(self):
        article_8 = articles(ENGLISH_URL)[7]
        assert article_8.name == "War crimes"

    def test_article_8_does_not_repeat_the_name(self):
        article_8 = articles(ENGLISH_URL)[7]
        assert article_8.text.startswith("1. The Court shall have jurisdiction")

    def test_article_9_has_correct_name(self):
        article_9 = articles(ENGLISH_URL)[9]
        assert article_9.name == "Elements of Crimes"

    def test_article_9_does_not_repeat_the_name(self):
        article_9 = articles(ENGLISH_URL)[9]
        assert article_9.text.startswith("1. Elements of Crimes shall assist")
