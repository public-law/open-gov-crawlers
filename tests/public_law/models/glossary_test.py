from ast import Call
from typing import Any, Callable, cast
from public_law.parsers.can.doj_glossaries import GlossaryParseResult, parse_glossary
from scrapy.http.response.html import HtmlResponse


def parsed_glossary_fixture(
    path: str, url: str, parse_func: Callable[[HtmlResponse], GlossaryParseResult]
) -> GlossaryParseResult:
    with open(f"tests/fixtures/{path}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_func(html)


GLOSSARY_FIXTURE = parsed_glossary_fixture(
    "index.html", "https://laws-lois.justice.gc.ca/eng/glossary/", parse_glossary
)


class TestAsDict:
    def it_returns_real_data(self):
        entries = cast(list[dict[str, Any]], GLOSSARY_FIXTURE.asdict()["entries"])
        assert entries[0]["phrase"] == "C.R.C."

    def it_converts_itself_to_a_dict(self):
        assert GLOSSARY_FIXTURE.asdict()

    def test_dict_func_doesnt_change_it(self):
        assert GLOSSARY_FIXTURE.asdict() == dict(GLOSSARY_FIXTURE.asdict())

    def test_dict_func_is_equivalent(self):
        assert GLOSSARY_FIXTURE.asdict() == dict(GLOSSARY_FIXTURE)

    def test_has_renamed_metadata_key(self):
        assert "dcterms:subject" in GLOSSARY_FIXTURE.asdict()["metadata"]
