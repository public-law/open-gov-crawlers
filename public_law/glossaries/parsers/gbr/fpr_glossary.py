from datetime import date, datetime

from bs4 import Tag
from scrapy.http.response.html import HtmlResponse

from public_law.glossaries.models.glossary import GlossaryEntry
from public_law.shared.utils.text import Sentence, ensure_ends_with_period, make_soup, cleanup


def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    """
    Parse the glossary entries from the HTML response.
    The entries are in a definition list (<dl>) with <dt> for terms and <dd> for definitions.
    """
    soup = make_soup(html)
    dl = soup.find("dl", class_="wp-block-simple-definition-list-blocks-list")
    if not dl or not isinstance(dl, Tag):
        return tuple()

    # Skip the header row (first dt/dd pair)
    terms = list(dl("dt"))[1:]  # Skip first dt
    definitions = list(dl("dd"))[1:]  # Skip first dd

    if not terms or not definitions or len(terms) != len(definitions):
        return tuple()

    return tuple(
        GlossaryEntry(
            phrase=cleanup(term.text),
            definition=Sentence(
                ensure_ends_with_period(
                    cleanup(defn.text.replace(
                        "“", '"').replace("”", '"'))
                )
            ),
        )
        for term, defn in zip(terms, definitions)
    )


def parse_mod_date(html: HtmlResponse) -> date:
    """
    Parse the modification date from the HTML.
    Format: "Monday, 30 January 2017"
    """
    try:
        soup = make_soup(html)
        date_span = soup.find("span", class_="right")
        if not date_span:
            return datetime.now().date()

        date_text = date_span.text
        date_str = date_text.replace("Updated: ", "").strip()

        return datetime.strptime(date_str, "%A, %d %B %Y").date()
    except Exception:
        return datetime.now().date()
