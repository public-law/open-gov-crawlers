from ast import Call
from typing import Any, Callable, TypeAlias, cast
from scrapy.http.response.html import HtmlResponse

from public_law.models.glossary import GlossaryParseResult
from public_law.parsers.can import doj_glossaries

ParseFunction: TypeAlias = Callable[[HtmlResponse], GlossaryParseResult]


def glossary_fixture(
    path: str, url: str, parse_func: ParseFunction
) -> GlossaryParseResult:
    with open(f"tests/fixtures/{path}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_func(html)


GLOSSARY = glossary_fixture(
    "index.html",
    "https://laws-lois.justice.gc.ca/eng/glossary/",
    doj_glossaries.parse_glossary,
)


class TestAsDict:
    def it_returns_real_data(self):
        entries = cast(list[dict[str, Any]], GLOSSARY.asdict()["entries"])
        assert entries[0]["phrase"] == "C.R.C."

    def it_converts_itself_to_a_dict(self):
        assert GLOSSARY.asdict()

    def test_dict_func_doesnt_change_it(self):
        assert GLOSSARY.asdict() == dict(GLOSSARY.asdict())

    def test_dict_func_is_equivalent(self):
        assert GLOSSARY.asdict() == dict(GLOSSARY)

    def test_has_renamed_metadata_key(self):
        assert "dcterms:subject" in GLOSSARY.asdict()["metadata"]
