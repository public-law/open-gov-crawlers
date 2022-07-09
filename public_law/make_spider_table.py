#!/usr/bin/env python

from dataclasses import dataclass
from types import ModuleType
from typing import Any, Literal, TypeAlias

import more_itertools

from .text import NonemptyString as String

CODE_REPO_BASE_URL = "https://github.com/public-law/open-gov-crawlers/blob/master"
DATA_REPO_BASE_URL = "https://github.com/public-law/datasets/blob/master"


LinkName: TypeAlias = Literal["parser", "spider", "tests", "json"]


def code_url(path: String) -> String:
    return String(f"{CODE_REPO_BASE_URL}/{path}")


def data_url(path: String) -> String:
    return String(f"{DATA_REPO_BASE_URL}/{path}")


def md_link(name: LinkName, url: String) -> String:
    return String(f"[{name}]({url})")


def code_link(name: LinkName, path: String) -> String:
    """
    Return a markdown-formatted link to the code repository.
    """
    return md_link(name, code_url(path))



@dataclass(frozen=True)
class SpiderRecordWithoutDataLink:
    """
    One row in the markdown table. It represents a spider whose output hasn't
    yet been published.
    """

    jd_verbose_name: String
    publication_name: String
    parser_path: String
    spider_path: String
    tests_path: String

    def as_markdown(self) -> str:
        """
        Return a markdown-formatted representation of this record.

        E.g.:   "Intergovernmental Rome Statute   [parser] | [spider] | [tests]"
        """
        return (
            f"| {self.jd_verbose_name} | {self.publication_name} "
            f"| {code_link('parser', self.parser_path)} \\|"
            f"  {code_link('spider', self.spider_path)} \\|"
            f"  {code_link('tests', self.tests_path)} | |"
        )


class SpiderRecord(SpiderRecordWithoutDataLink):
    """
    One row in the markdown table.
    """
    json_path: String  # Can be an empty string if there is no public dataset yet.

    def __init__(self, json_path: String, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.json_path = json_path

    def as_markdown(self) -> str:
        """
        Return a markdown-formatted representation of this record.

        E.g.:   "Intergovernmental Rome Statute   [parser] | [spider] | [tests]   [json]"
        """
        return (
            f"| {self.jd_verbose_name} | {self.publication_name} "
            f"| {code_link('parser', self.parser_path)} \\|"
            f"  {code_link('spider', self.spider_path)} \\|"
            f"  {code_link('tests', self.tests_path)} "
            f"| {self.json_link} |"
        )

    @property
    def json_link(self) -> str:
        return md_link("json", data_url(String(self.json_path)))


@dataclass(frozen=True)
class MarkdownTable:
    """
    A table of spider records.
    """

    records: tuple[SpiderRecord|SpiderRecordWithoutDataLink, ...]

    def as_markdown(self) -> str:
        """
        Return a string representation of this table.
        """

        # fmt: off
        heading = (
            "|   |   | Source code | Dataset |\n"
            "| - | - | :---------- | :------ |\n"
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


def file_path(module: ModuleType) -> str:
    match module.__file__:
        case str(filename):
            return "/".join(more_itertools.tail(2, filename.split("/")))
        case None:
            raise ValueError(f"Module {module} has no __file__ attribute")


def tests_path(module: ModuleType) -> str:
    return file_path(module).replace(".py", "_test.py")


def make_record(module: ModuleType, json_path: String) -> SpiderRecord:
    return SpiderRecord(
        json_path=json_path,
        jd_verbose_name=String(module.JD_VERBOSE_NAME),
        publication_name=String(module.PUBLICATION_NAME),
        parser_path=String(f"public_law/parsers/{file_path(module)}"),
        spider_path=String(f"public_law/spiders/{file_path(module)}"),
        tests_path=String(f"tests/public_law/parsers/{tests_path(module)}"),
    )

def make_record_without_dataset(module: ModuleType) -> SpiderRecordWithoutDataLink:
    return SpiderRecordWithoutDataLink(
        jd_verbose_name=String(module.JD_VERBOSE_NAME),
        publication_name=String(module.PUBLICATION_NAME),
        parser_path=String(f"public_law/parsers/{file_path(module)}"),
        spider_path=String(f"public_law/spiders/{file_path(module)}"),
        tests_path=String(f"tests/public_law/parsers/{tests_path(module)}"),
    )


#
# Execution begins here.
#

from .spiders.can import doj_glossaries
from .spiders.int import rome_statute
from .spiders.irl import courts_glossary
from .spiders.nzl import justice_glossary
from .spiders.usa import georgia_ag_opinions, oregon_regs, us_courts_glossary

TABLE = MarkdownTable(
    (
        make_record(courts_glossary,     String("Ireland/courts-glossary.json")),
        make_record(doj_glossaries,      String("Canada/doj-glossaries.json")),
        make_record(justice_glossary,    String("NewZealand/justice-glossary.json")),
        make_record(rome_statute,        String("Intergovernmental/RomeStatute/RomeStatute.json")),
        make_record(us_courts_glossary,  String("UnitedStates/us-courts-glossary.json")),
        make_record_without_dataset(georgia_ag_opinions),
        make_record_without_dataset(oregon_regs),
    )
)
