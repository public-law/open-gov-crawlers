#!/usr/bin/env python

from dataclasses import dataclass
from typing import Any

import more_itertools

CODE_REPO_BASE_URL = "https://github.com/public-law/open-gov-crawlers/blob/master"
DATA_REPO_BASE_URL = "https://github.com/public-law/datasets/blob/master"


def _code_url(path: str) -> str:
    match path:
        case "":
            return ""
        case _:
            return f"{CODE_REPO_BASE_URL}/{path}"


def _data_url(path: str) -> str:
    match path:
        case "":
            return ""
        case _:
            return f"{DATA_REPO_BASE_URL}/{path}"


def _md_anchor(name: str, url: str) -> str:
    match url:
        case "":
            return ""
        case _:
            return f"[{name}]({url})"


@dataclass(frozen=True)
class SpiderRecord:
    """
    One row in the markdown table.
    """

    jd_verbose_name: str
    publication_name: str
    parser_path: str
    spider_path: str
    tests_path: str
    json_path: str

    def as_markdown(self) -> str:
        """
        Return a string representation of this record.
        """
        return f"| {self.jd_verbose_name} | {self.publication_name} | [parser]({self.parser_url()}) | [spider]({self.spider_url()}) | [tests]({self.tests_url()}) | {self.json_md} |"

    def parser_url(self) -> str:
        return _code_url(self.parser_path)

    def spider_url(self) -> str:
        return _code_url(self.spider_path)

    def tests_url(self) -> str:
        return _code_url(self.tests_path)

    @property
    def json_md(self) -> str:
        return _md_anchor("JSON Output", _data_url(self.json_path))


@dataclass(frozen=True)
class MarkdownTable:
    """
    A table of spider records.
    """

    records: tuple[SpiderRecord, ...]

    def as_markdown(self) -> str:
        """
        Return a string representation of this table.
        """
        heading = (
            "| Jurisdiction | Publication | Parser | Spider | Tests | JSON Output |\n"
            "| ------------ | ----------- | ------ | ------ | ----- | ----------- |\n"
        )

        body = "\n".join(
            [
                r.as_markdown()
                for r in sorted(
                    self.records, key=lambda r: (r.jd_verbose_name, r.publication_name)
                )
            ]
        )

        return heading + body


from .spiders.usa import georgia_ag_opinions
from .spiders.usa import us_courts_glossary


def file_path(module: Any) -> str:
    return "/".join(more_itertools.tail(2, module.__file__.split("/")))


def test_path(module: Any) -> str:
    return file_path(module).replace(".py", "test.py")


# fmt: off
TABLE = MarkdownTable(
    records=(
        SpiderRecord(
            jd_verbose_name =  georgia_ag_opinions.JD_VERBOSE_NAME,
            publication_name = georgia_ag_opinions.PUBLICATION_NAME,
            parser_path =      f"public_law/parsers/{file_path(georgia_ag_opinions)}",
            spider_path =      f"public_law/spiders/{file_path(georgia_ag_opinions)}",
            tests_path  =      f"tests/public_law/parsers/{test_path(georgia_ag_opinions)}",
            json_path   =      "",
        ),
        SpiderRecord(
            jd_verbose_name =  us_courts_glossary.JD_VERBOSE_NAME,
            publication_name = us_courts_glossary.PUBLICATION_NAME,
            parser_path =      "public_law/parsers/usa/us_courts_glossary.py",
            spider_path =      "public_law/spiders/usa/us_courts_glossary.py",
            tests_path  =      "tests/public_law/parsers/usa/us_courts_glossary_test.py",
            json_path   =      "UnitedStates/us-courts-glossary.json",
        ),
    )
)
