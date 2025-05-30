[![Test Suite](https://github.com/public-law/open-gov-crawlers/actions/workflows/python-app.yml/badge.svg)](https://github.com/public-law/open-gov-crawlers/actions/workflows/python-app.yml)


# Open-gov spiders written in Python

Crawlers and parsers for extracting legal glossary and regulation data from official government sources. This repository powers 
[Public.Law](https://www.public.law)’s free legal dictionary and statute archive. Each source has a dedicated spider, parser, and test module.


|                   |                                                                                                                                                                   | Source code                                                                                                                                                                                                                                                                                                                                                                                  | Dataset                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| Australia         | [Family, domestic and sexual violence...](https://www.public.law/dictionary/sources/aihw.gov.au__reports-data_behaviours-risk-factors_domestic-violence_glossary) | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/aus/dv_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/aus/dv_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/aus/dv_glossary_test.py)                                  | [`json`](https://github.com/public-law/datasets/blob/master/Australia/dv-glossary.json)                     |
| Australia         | [IP Glossary](https://www.public.law/dictionary/sources/ipaustralia.gov.au__tools-resources_ip-glossary)                                                          | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/aus/ip_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/aus/ip_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/aus/ip_glossary_test.py)                                  | [`json`](https://github.com/public-law/datasets/blob/master/Australia/ip-glossary.json)                     |
| Canada            | [Dept. of Justice Legal Glossaries](https://www.public.law/dictionary/sources)                                                                                    | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/can/doj_glossaries.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/can/doj_glossaries.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/can/doj_glossaries_test.py)                         | [`json`](https://github.com/public-law/datasets/blob/master/Canada/doj-glossaries.json)                     |
| Canada            | [Glossary of Parliamentary Terms for...](https://www.public.law/dictionary/sources/lop.parl.ca__About_Parliament_Education_glossary-intermediate-students-e)      | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/can/parliamentary_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/can/parliamentary_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/can/parliamentary_glossary_test.py) | [`json`](https://github.com/public-law/datasets/blob/master/Canada/parliamentary-glossary.json)             |
| Intergovernmental | [Rome Statute](https://world.public.law/rome_statute)                                                                                                             | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/int/rome_statute.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/int/rome_statute.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/int/rome_statute_test.py)                               | [`json`](https://github.com/public-law/datasets/blob/master/Intergovernmental/RomeStatute/RomeStatute.json) |
| Ireland           | [Glossary of Legal Terms](https://www.public.law/dictionary/sources/courts.ie__glossary)                                                                          | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/irl/courts_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/irl/courts_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/irl/courts_glossary_test.py)                      | [`json`](https://github.com/public-law/datasets/blob/master/Ireland/courts-glossary.json)                   |
| New Zealand       | [Glossary](https://www.public.law/dictionary/sources/justice.govt.nz__about_glossary)                                                                             | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/nzl/justice_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/nzl/justice_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/nzl/justice_glossary_test.py)                   | [`json`](https://github.com/public-law/datasets/blob/master/NewZealand/justice-glossary.json)               |
| USA               | [US Courts Glossary](https://www.public.law/dictionary/sources/uscourts.gov__glossary)                                                                            | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/usa/us_courts_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/usa/us_courts_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/usa/us_courts_glossary_test.py)             | [`json`](https://github.com/public-law/datasets/blob/master/UnitedStates/us-courts-glossary.json)           |
| USA               | [USCIS Glossary](https://www.public.law/dictionary/sources/uscis.gov__tools_glossary)                                                                             | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/usa/uscis_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/usa/uscis_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/usa/uscis_glossary_test.py)                         | [`json`](https://github.com/public-law/datasets/blob/master/UnitedStates/uscis-glossary.json)               |
| USA / Georgia     | Attorney General Opinions                                                                                                                                         | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/usa/georgia_ag_opinions.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/usa/georgia_ag_opinions.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/usa/georgia_ag_opinions_test.py)          |                                                                                                             |
| USA / Oregon      | [Oregon Administrative Rules](https://oregon.public.law/rules)                                                                                                    | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/usa/oregon_regs.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/spiders/usa/oregon_regs.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/public_law/parsers/usa/oregon_regs_test.py)                                  |                                                                                                             |



> The [USA Courts Glossary parser](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/parsers/usa/courts_glossary.py)
> is the best example of our coding style.
> See [the wiki](https://github.com/public-law/open-gov-crawlers/wiki) for a deep dive explanation
> of our parsing strategy. 


## Example: USA Courts Glossary Parser
The spiders retrieve HTML pages and output well formed JSON. Glossary parsers
all output the same JSON format.

First, we can see which spiders are available:

```bash
$ scrapy list

aus_ip_glossary
can_doj_glossaries
int_rome_statute
...
```

Then we can run one of the spiders, e.g. the USA Courts Glossary:

```bash
$ scrapy crawl --overwrite-output tmp/output.json usa_courts_glossary
```

This produces:

```json
[
  ...
  {
    "phrase": "Sentence",
    "definition": "The punishment ordered by a court for a defendant convicted of a crime."
  },
  {
    "phrase": "Sentencing guidelines",
    "definition": "A set of rules and principles established by the United States Sentencing Commission that trial judges use to determine the sentence for a convicted defendant."
  },
  {
    "phrase": "Sequester",
    "definition": "To separate. Sometimes juries are sequestered from outside influences during their deliberations."
  },
  ...
]
```


Development Environment Notes
-----------------------------

### Python 3.10 or greater

I'm using [asdf](https://asdf-vm.com/#/) because the Homebrew distribution
is more up-to-date than pyenv.


### [Poetry](https://python-poetry.org/) for dependency management

Making sure I have the current deps installed is always good to do:

```bash
poetry install
```

### Pytest for testing

The pytest tests run easily:

```bash
poetry run pytest
```

## Other tools

* Java is required by the Python Tika package.
* Pylance/Pyright for type-checking
* Black for formatting


### Dependencies; helpful links

* [The Scrapy Playbook](https://thepythonscrapyplaybook.com)

## Contributing

To add a new glossary crawler:

1. Pick a source and add a new spider under `public_law/spiders/`.
2. Write a parser in `public_law/parsers/` that extracts terms and metadata.
3. Add a test case under `tests/public_law/parsers/`.
4. Run the spider using `scrapy crawl --overwrite-output tmp/output.json`.

Need help? Just ask in GitHub Issues or ping @robb.
