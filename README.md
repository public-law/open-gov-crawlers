![Test Suite](https://github.com/public-law/scrapy-spiders/workflows/Test%20Suite/badge.svg)


# Open-gov spiders written with Python/Scrapy

| Publication |   |   |   |
| - | - | - | - |
| Canada / Dept. of Justice Legal Glossaries | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/ca/doj.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/ca/doj_glossaries.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/ca/doj_glossaries_test.py) |
| U.S.A. / Georgia Attorney General Opinions | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/us/georgia.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/us/georgia_ag_opinions.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/ga_parsers_test.py) |
| U.S.A. / Oregon Regulations | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/us/oregon.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/us/oregon_regs.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/oar_parsers_test.py) |


## Example: Oregon Administrative Rules Parser
The spiders retrieve the HTML pages and output well formed JSON which represents the source's structure:

```bash
$ scrapy crawl secure.sos.state.or.us
```

This produces the output:

```json
{
  "date_accessed": "2019-03-21",
  "chapters": [
    {
      "kind": "Chapter",
      "db_id": "36",
      "number": "101",
      "name": "Oregon Health Authority, Public Employees' Benefit Board",
      "url": "https://secure.sos.state.or.us/oard/displayChapterRules.action?selectedChapter=36",
      "divisions": [
        {
          "kind": "Division",
          "db_id": "1",
          "number": "1",
          "name": "Procedural Rules",
          "url": "https://secure.sos.state.or.us/oard/displayDivisionRules.action?selectedDivision=1",
          "rules": [
            {
              "kind": "Rule",
              "number": "101-001-0000",
              "name": "Notice of Proposed Rule Changes",
              "url": "https://secure.sos.state.or.us/oard/view.action?ruleNumber=101-001-0000",
              "authority": [
                "ORS 243.061 - 243.302"
              ],
              "implements": [
                "ORS 183.310 - 183.550",
                "192.660",
                "243.061 - 243.302",
                "292.05"
              ],
              "history": "PEBB 2-2009, f. 7-29-09, cert. ef. 8-1-09<br>PEBB 1-2009(Temp), f. &amp; cert. ef. 2-24-09 thru 8-22-09<br>PEBB 1-2004, f. &amp; cert. ef. 7-2-04<br>PEBB 1-1999, f. 12-8-99, cert. ef. 1-1-00",
              }
            ]
          }
        ]
      }
    ]
  }
```
(etc.)


Development Environment Notes
-----------------------------

Run the pytest tests like this:

```bash
pytest
```
