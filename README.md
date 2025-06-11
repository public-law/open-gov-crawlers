[![Test Suite](https://github.com/public-law/open-gov-crawlers/actions/workflows/python-app.yml/badge.svg)](https://github.com/public-law/open-gov-crawlers/actions/workflows/python-app.yml)


# Open-gov spiders written in Python

Crawlers and parsers for extracting legal glossary and regulation data from official government sources. This repository powers 
[Public.Law](https://www.public.law)'s free legal dictionary and statute archive. Each source has a dedicated spider, parser, and test module.

## Repository Structure

The repository is organized by business domain rather than technology:

```
public_law/
├── glossaries/          # Legal glossary crawlers
│   ├── models/            # Data models for glossary entries
│   ├── parsers/           # HTML parsing logic by jurisdiction
│   └── spiders/           # Scrapy spiders by jurisdiction
├── legal_texts/         # Legal document crawlers
│   ├── models/            # Data models for legal documents
│   ├── parsers/           # Document parsing logic
│   └── spiders/           # Document crawling spiders
└── shared/              # Shared components
    ├── exceptions/        # Custom exceptions
    ├── models/            # Base data models
    ├── spiders/           # Base spider classes
    └── utils/             # Common utilities
```

## Architecture

Our glossary crawling system follows a clean separation of concerns between **data extraction** and **configuration management**:

### Before: Monolithic Parser Architecture
```
Parser = HTML extraction + metadata creation
```

### After: Separated Spider/Parser Architecture
```
Parser = Pure HTML extraction (parse_entries())
Spider = Configuration + orchestration (get_metadata() + inherited parse_glossary())
```

### Key Components

**Parsers** (`public_law/glossaries/parsers/`):
- **Pure functions** that extract glossary entries from HTML
- Export only `parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]`
- No metadata creation, no side effects
- Easily testable in isolation

**Spiders** (`public_law/glossaries/spiders/`):
- Inherit from `EnhancedAutoGlossarySpider` base class
- Implement `get_metadata(response: HtmlResponse) -> Metadata` method
- Handle all configuration: URLs, Dublin Core metadata, subjects
- Orchestrate the parsing process via inherited `parse_glossary()`

**Base Classes** (`public_law/shared/spiders/`):
- `EnhancedAutoGlossarySpider`: Provides `parse_glossary()` orchestration
- Automatically resolves and calls the appropriate parser
- Combines parser output with spider metadata

### Benefits

**🔄 DRY (Don't Repeat Yourself)**:
- `parse_glossary()` orchestration logic written once in base class
- No duplication of parsing workflow across spiders

**🛡️ Type Safety**:
- All configuration data strongly typed in Python
- Compile-time validation of metadata structure
- IDE support for autocompletion and refactoring

**🎯 Separation of Concerns**:
- **Parsers**: Focus solely on HTML → data extraction
- **Spiders**: Focus solely on configuration and orchestration
- Clear boundaries make the system easier to understand and maintain

**🧪 Testability**:
- Parsers can be tested independently with just HTML fixtures
- Spiders can be tested independently for metadata correctness
- Integration tests verify the complete workflow
- Faster test execution due to focused test scope

**🔧 Maintainability**:
- Changes to parsing logic isolated to parser modules
- Changes to metadata/configuration isolated to spider modules
- Base class improvements benefit all spiders automatically

### Example Usage

```python
# Parser: Pure data extraction
def parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = from_response(html)
    return tuple(
        GlossaryEntry(phrase=..., definition=...)
        for entry in soup.find_all("dt")
    )

# Spider: Configuration + orchestration
class MyGlossarySpider(EnhancedAutoGlossarySpider):
    name = "jurisdiction_source_glossary"
    start_urls = ["https://example.gov/glossary"]
    
    def get_metadata(self, response: HtmlResponse) -> Metadata:
        return Metadata(
            dcterms_title="My Glossary",
            dcterms_coverage="USA",
            dcterms_subject=(...),
            # ... other Dublin Core metadata
        )
```

The spider automatically calls the parser and combines results:
```python
result = spider.parse_glossary(response)
# result.entries from parser
# result.metadata from spider
```

## Data Sources

|                   |                                                                                                                                                                   | Source code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Dataset                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------- |
| Australia         | [Family, domestic and sexual violence...](https://www.public.law/dictionary/sources/aihw.gov.au__reports-data_behaviours-risk-factors_domestic-violence_glossary) | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/aus/dv_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/aus/dv_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/aus/dv_glossary_test.py)                                                                                                                                                           | [`json`](https://github.com/public-law/datasets/blob/master/Australia/dv-glossary.json)                     |
| Australia         | [IP Glossary](https://www.public.law/dictionary/sources/ipaustralia.gov.au__tools-resources_ip-glossary)                                                          | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/aus/ip_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/aus/ip_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/aus/ip_glossary_test.py)                                                                                                                                                           | [`json`](https://github.com/public-law/datasets/blob/master/Australia/ip-glossary.json)                     |
| Australia         | [Design IP Glossary](https://www.public.law/dictionary/sources/ipaustralia.gov.au__design_glossary)                                                               | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/aus/designip_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/aus/designip_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/aus/designip_glossary_test.py)                                                                                                                                         | [`json`](https://github.com/public-law/datasets/blob/master/Australia/designip-glossary.json)               |
| Australia         | [Law Handbook Glossary](https://www.public.law/dictionary/sources/lawhandbook.sa.gov.au__go01)                                                                    | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/aus/lawhandbook_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/aus/lawhandbook_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/aus/lawhandbook_glossary_test.py)                                                                                                                                | [`json`](https://github.com/public-law/datasets/blob/master/Australia/lawhandbook-glossary.json)            |
| Canada            | [Parliamentary Glossary](https://www.public.law/dictionary/sources/lop.parl.ca__About_Parliament_Education_glossary-intermediate-students-e)                      | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/can/parliamentary_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/can/parliamentary_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/can/parliamentary_glossary_test.py)                                                                                                                          | [`json`](https://github.com/public-law/datasets/blob/master/Canada/parliamentary-glossary.json)             |
| Canada            | [Patents Glossary](https://www.public.law/dictionary/sources/ised-isde.canada.ca__patents_glossary)                                                               | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/can/patents_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/can/patents_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/can/patents_glossary_test.py)                                                                                                                                            | [`json`](https://github.com/public-law/datasets/blob/master/Canada/patents-glossary.json)                   |
| Great Britain     | [Criminal Procedure Rules Glossary](https://www.public.law/dictionary/sources/legislation.gov.uk__uksi_2020_759_part_Glossary)                                    | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/gbr/cpr_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/gbr/cpr_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/gbr/cpr_glossary_test.py)                                                                                                                                                        | [`json`](https://github.com/public-law/datasets/blob/master/GreatBritain/cpr-glossary.json)                 |
| Great Britain     | [Family Procedure Rules Glossary](https://www.public.law/dictionary/sources/justice.gov.uk__courts_procedure-rules_family_backmatter_fpr_glossary)                | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/gbr/fpr_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/gbr/fpr_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/gbr/fpr_glossary_test.py)                                                                                                                                                        | [`json`](https://github.com/public-law/datasets/blob/master/GreatBritain/fpr-glossary.json)                 |
| Ireland           | [Courts Glossary](https://www.public.law/dictionary/sources/courts.ie__glossary)                                                                                  | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/irl/courts_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/irl/courts_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/irl/courts_glossary_test.py)                                                                                                                                               | [`json`](https://github.com/public-law/datasets/blob/master/Ireland/courts-glossary.json)                   |
| New Zealand       | [Justice Glossary](https://www.public.law/dictionary/sources/justice.govt.nz__about_glossary)                                                                     | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/nzl/justice_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/nzl/justice_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/nzl/justice_glossary_test.py)                                                                                                                                            | [`json`](https://github.com/public-law/datasets/blob/master/NewZealand/justice-glossary.json)               |
| USA               | [US Courts Glossary](https://www.public.law/dictionary/sources/uscourts.gov__glossary)                                                                            | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/usa/courts_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/usa/courts_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/usa/courts_glossary_test.py)                                                                                                                                               | [`json`](https://github.com/public-law/datasets/blob/master/UnitedStates/us-courts-glossary.json)           |
| USA               | [USCIS Glossary](https://www.public.law/dictionary/sources/uscis.gov__tools_glossary)                                                                             | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/usa/uscis_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/usa/uscis_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/usa/uscis_glossary_test.py)                                                                                                                                                  | [`json`](https://github.com/public-law/datasets/blob/master/UnitedStates/uscis-glossary.json)               |
| USA               | [Criminal Glossary](https://www.public.law/dictionary/sources/sdcourt.ca.gov__sdcourt_criminal2_criminalglossary)                                                 | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/usa/criminal_glossary.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/usa/criminal_glossary.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/parsers/usa/criminal_glossary_test.py) \| [`spider tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/glossaries/spiders/usa/criminal_glossary_test.py) | [`json`](https://github.com/public-law/datasets/blob/master/UnitedStates/criminal-glossary.json)            |
| Intergovernmental | [Rome Statute](https://world.public.law/rome_statute)                                                                                                             | [`parser`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/legal_texts/parsers/int/rome_statute.py) \|  [`spider`](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/legal_texts/spiders/int/rome_statute.py) \|  [`tests`](https://github.com/public-law/open-gov-crawlers/blob/master/tests/legal_texts/parsers/int/rome_statute_test.py)                                                                                                                                                     | [`json`](https://github.com/public-law/datasets/blob/master/Intergovernmental/RomeStatute/RomeStatute.json) |


> [!TIP]
> The [USA Courts Glossary](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/spiders/usa/courts_glossary.py) spider and [parser](https://github.com/public-law/open-gov-crawlers/blob/master/public_law/glossaries/parsers/usa/courts_glossary.py)
> are the best examples of our new architecture and coding style.


## Example: USA Courts Glossary Parser
The spiders retrieve HTML pages and output well formed JSON. Glossary parsers
all output the same JSON format.

First, we can see which spiders are available:

```bash
$ scrapy list

aus_designip_glossary
aus_dv_glossary
aus_ip_glossary
aus_lawhandbook_glossary
can_parliamentary_glossary
can_patents_glossary
gbr_cpr_glossary
gbr_fpr_glossary
int_rome_statute
irl_courts_glossary
nzl_justice_glossary
usa_courts_glossary
usa_criminal_glossary
usa_uscis_glossary
...
```

Then we can run one of the spiders, e.g. the USA Courts Glossary:

```bash
$ scrapy crawl --overwrite-output tmp/output.json usa_courts_glossary
```

Here's a snippet of the output:

```json
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
```

> [!NOTE]
> See [the wiki](https://github.com/public-law/open-gov-crawlers/wiki) for a deep dive explanation
> of our parsing strategy. 


Development Environment Notes
-----------------------------

### Python 3.12

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

I run them automatically when a file changes using pytest-watcher.
It's automatically installed with the project:

```bash
poetry run ptw .
```

## Other tools

* Java is required by the Python Tika package.
* Pylance/Pyright for type-checking


### Dependencies; helpful links

* [The Scrapy Playbook](https://thepythonscrapyplaybook.com)

## Contributing

To add a new glossary crawler:

1. **Create the parser** in `public_law/glossaries/parsers/{jurisdiction}/`:
   - Write a pure `parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]` function
   - Focus only on HTML → data extraction, no metadata
   - Add parser tests under `tests/glossaries/parsers/{jurisdiction}/`

2. **Create the spider** in `public_law/glossaries/spiders/{jurisdiction}/`:
   - Inherit from `EnhancedAutoGlossarySpider`
   - Implement `get_metadata(response: HtmlResponse) -> Metadata` method
   - Configure `name` and `start_urls` attributes
   - Add spider tests under `tests/glossaries/spiders/{jurisdiction}/`

3. **Test and run**:
   - Run tests: `poetry run pytest tests/glossaries/{parser,spiders}/{jurisdiction}/`
   - Run spider: `scrapy crawl --overwrite-output tmp/output.json {spider_name}`

To add a new legal text crawler:

1. Add a new spider under `public_law/legal_texts/spiders/{jurisdiction}/`.
2. Write a parser in `public_law/legal_texts/parsers/{jurisdiction}/` that extracts document structure and metadata.
3. Add a test case under `tests/legal_texts/parsers/{jurisdiction}/`.
4. Run the spider using `scrapy crawl --overwrite-output tmp/output.json {spider_name}`.

The repository follows a business-domain-first organization:
- **Glossaries**: Legal term definitions and dictionaries
- **Legal Texts**: Full legal documents, statutes, and regulations
- **Shared**: Common utilities, base classes, and models used across domains

Need help? Just ask in GitHub Issues or ping @robb.
