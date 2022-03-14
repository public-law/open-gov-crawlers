![Test Suite](https://github.com/public-law/scrapy-spiders/workflows/Test%20Suite/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/6b1458d526c7233e6703/maintainability)](https://codeclimate.com/github/public-law/scrapy-spiders/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6b1458d526c7233e6703/test_coverage)](https://codeclimate.com/github/public-law/scrapy-spiders/test_coverage)


# Open-gov spiders written with Python/Scrapy

| Publication |   |   |   |
| - | - | - | - |
| Canada / Dept. of Justice Legal Glossaries | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/ca/doj.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/ca/doj_glossaries.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/ca/doj_glossaries_test.py) |
| U.S.A. / Georgia Attorney General Opinions | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/us/georgia.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/us/georgia_ag_opinions.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/us/ga_parsers_test.py) |
| U.S.A. / Oregon Regulations | [parser](https://github.com/public-law/scrapy-spiders/blob/master/public_law/parsers/us/oregon.py) | [spider](https://github.com/public-law/scrapy-spiders/blob/master/public_law/spiders/us/oregon_regs.py) | [tests](https://github.com/public-law/scrapy-spiders/blob/master/test/us/oar_parsers_test.py) |

> FYI: We're looking for help writing more spiders like these. [See the wiki](https://github.com/public-law/open-gov-crawlers/wiki) for a technical explanation
> of our parsing strategy.


## Example: Oregon Administrative Rules Parser
The spiders retrieve the HTML pages and output well formed JSON which represents the source's structure.
First, we can see which spiders are available:

```bash
$ scrapy list

canada_doj_glossaries
georgia_ag_opinions
oregon_regs
```

Then we can run one of the spiders:

```bash
$ scrapy crawl oregon_regs
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

[The Wiki](https://github.com/public-law/open-gov-crawlers/wiki) explains the JSON strategy.


Development Environment Notes
-----------------------------

### Python 3.9

I'm personally using
[pyenv](https://github.com/pyenv/pyenv) to install Python, but
[asdf](https://asdf-vm.com/#/) is a good option too.


### [Poetry](https://python-poetry.org/) for dependency management

So before I start working, I go into the virtual environment:

```bash
poetry shell
```

Making sure I have the current deps installed is always good to do:

```bash
poetry install
```

### Pytest for testing

The pytest tests run easily:

```bash
pytest
```

I use this to monitor and retest automatically as I work. There might be better ways
to do this:

```bash
watchmedo shell-command --command='clear ; pytest' --patterns="*.py" --recursive .
```

### Dependencies; helpful links

* [The Zyte runtime environments](https://github.com/scrapinghub/scrapinghub-stack-scrapy)
* [SHUB Configuration](https://shub.readthedocs.io/en/stable/configuration.html)
