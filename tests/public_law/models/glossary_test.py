from public_law.parsers.can.doj_glossaries import GlossaryParseResult, parse_glossary
from scrapy.http.response.html import HtmlResponse


def parsed_fixture(filename: str, url: str) -> GlossaryParseResult:
    with open(f"tests/fixtures/{filename}", encoding="utf8") as f:
        html = HtmlResponse(
            url=url,
            body=f.read(),
            encoding="UTF-8",
        )

    return parse_glossary(html)


def laws_lois() -> GlossaryParseResult:
    return parsed_fixture("index.html", "https://laws-lois.justice.gc.ca/eng/glossary/")


GLOSSARY_FIXTURE = laws_lois()


class TestAsDict:
    def it_returns_real_data(self):
        assert GLOSSARY_FIXTURE.asdict()["entries"][0]["phrase"] == "C.R.C."

    def it_converts_itself_to_a_dict(self):
        assert GLOSSARY_FIXTURE.asdict()

    def test_dict_func_doesnt_change_it(self):
        assert GLOSSARY_FIXTURE.asdict() == dict(GLOSSARY_FIXTURE.asdict())

    def test_dict_func_is_equivalent(self):
        assert GLOSSARY_FIXTURE.asdict() == dict(GLOSSARY_FIXTURE)
