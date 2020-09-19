from scrapy.http import HtmlResponse
from public_law.parsers.ca.doj import parse_glossary


def parsed_glossary() -> GlossarySourceParseResult:
    filename = "www.justice.gc.ca_eng_rp-pr_cp-pm_eval_rep-rap_12_lap-paj_p7g.html"

    with open(f"test/fixtures/{filename}") as f:
        html = HtmlResponse(
            url="https://www.justice.gc.ca/eng/rp-pr/cp-pm/eval/rep-rap/12/lap-paj/p7g.html",
            body=f.read(),
            encoding="UTF-8",
        )
        return parse_glossary(html)


class ParseGlossaryTest:
    pass
