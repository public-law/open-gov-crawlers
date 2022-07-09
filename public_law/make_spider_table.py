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
        return f"| {self.jd_verbose_name} | {self.publication_name} | [parser]({self.parser_url()}), [spider]({self.spider_url()}), [tests]({self.tests_url()}) | {self.json_md} |"

    def parser_url(self) -> str:
        return _code_url(self.parser_path)

    def spider_url(self) -> str:
        return _code_url(self.spider_path)

    def tests_url(self) -> str:
        return _code_url(self.tests_path)

    @property
    def json_md(self) -> str:
        return _md_anchor("json", _data_url(self.json_path))


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
            "| Jurisdiction | Publication | Source code | Dataset |\n"
            "| :----------- | :---------- | :---------- | :------ |\n"
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


def file_path(module: Any) -> str:
    return "/".join(more_itertools.tail(2, module.__file__.split("/")))


def tests_path(module: Any) -> str:
    return file_path(module).replace(".py", "test.py")


def make_record(module: Any, json_path: str = "") -> SpiderRecord:
    return SpiderRecord(
        jd_verbose_name=module.JD_VERBOSE_NAME,
        publication_name=module.PUBLICATION_NAME,
        parser_path=f"public_law/parsers/{file_path(georgia_ag_opinions)}",
        spider_path=f"public_law/spiders/{file_path(georgia_ag_opinions)}",
        tests_path=f"tests/public_law/parsers/{tests_path(georgia_ag_opinions)}",
        json_path=json_path,
    )


#
# Execution begins here.
#

from .spiders.can import doj_glossaries
from .spiders.int import rome_statute
from .spiders.irl import courts_glossary
from .spiders.nzl import justice_glossary
from .spiders.usa import georgia_ag_opinions, us_courts_glossary, oregon_regs

# fmt: off
TABLE = MarkdownTable(
    (
        make_record(courts_glossary,     "Ireland/courts-glossary.json"),
        make_record(doj_glossaries,      "Canada/doj-glossaries.json"),
        make_record(georgia_ag_opinions),
        make_record(justice_glossary,    "NewZealand/justice-glossary.json"),
        make_record(oregon_regs),
        make_record(rome_statute,        "Intergovernmental/RomeStatute/RomeStatute.json"),
        make_record(us_courts_glossary,  "UnitedStates/us-courts-glossary.json"),
    )
)
