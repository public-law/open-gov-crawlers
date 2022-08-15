from dataclasses import dataclass
from types import ModuleType
from typing import Any, Literal, TypeAlias

import more_itertools

from .text import NonemptyString as String, truncate_words

CODE_REPO_BASE_URL = "https://github.com/public-law/open-gov-crawlers/blob/master"
DATA_REPO_BASE_URL = "https://github.com/public-law/datasets/blob/master"


#
# By using NonemptyString and this Literal, we don't need to
# write explicit error checking.
#
LinkName: TypeAlias = Literal["parser", "spider", "tests", "json"]


def code_url(path: String) -> String:
    return String(f"{CODE_REPO_BASE_URL}/{path}")


def data_url(path: String) -> String:
    return String(f"{DATA_REPO_BASE_URL}/{path}")


def md_link(name: str, url: String) -> String:
    return String(f"[{name}]({url})")


def code_link(name: LinkName, path: String) -> String:
    """
    Return a markdown-formatted link to the code repository.
    """
    return String(md_link(f"`{name}`", code_url(path)))



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
    web_url: str | None = None

    def as_markdown(self) -> str:
        """
        Return a markdown-formatted representation of this record.

        E.g.:   "Intergovernmental Rome Statute   [parser] | [spider] | [tests]"
        """
        if self.web_url:
            pub = f"[{self.truncated_pub_name}]({self.web_url})"
        else:
            pub = self.truncated_pub_name

        return (
            f"| {self.jd_verbose_name} | {pub} "
            f"| {code_link('parser', self.parser_path)} \\|"
            f"  {code_link('spider', self.spider_path)} \\|"
            f"  {code_link('tests', self.tests_path)} | |"
        )

    @property
    def truncated_pub_name(self) -> str:
        """
        Return a truncated version of the publication name.
        """
        return truncate_words(self.publication_name, 5)


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
        if self.web_url:
            pub = f"[{self.truncated_pub_name}]({self.web_url})"
        else:
            pub = self.truncated_pub_name

        return (
            f"| {self.jd_verbose_name} | {pub} "
            f"| {code_link('parser', self.parser_path)} \\|"
            f"  {code_link('spider', self.spider_path)} \\|"
            f"  {code_link('tests', self.tests_path)} "
            f"| {self.json_link} |"
        )

    @property
    def json_link(self) -> str:
        return code_link("json", data_url(String(self.json_path)))


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


#
# By using two different types for the markdown rows, and two
# different factory methods, we don't need any branching statements.
#

def make_record(module: ModuleType, json_path: String, web_url: str|None = None) -> SpiderRecord:
    return SpiderRecord(
        json_path=json_path,
        jd_verbose_name=String(module.JD_VERBOSE_NAME),
        publication_name=String(module.PUBLICATION_NAME),
        parser_path=String(f"public_law/parsers/{file_path(module)}"),
        spider_path=String(f"public_law/spiders/{file_path(module)}"),
        tests_path=String(f"tests/public_law/parsers/{tests_path(module)}"),
        web_url=web_url,
    )

def make_record_without_dataset(module: ModuleType, web_url: str|None = None) -> SpiderRecordWithoutDataLink:
    return SpiderRecordWithoutDataLink(
        jd_verbose_name=String(module.JD_VERBOSE_NAME),
        publication_name=String(module.PUBLICATION_NAME),
        parser_path=String(f"public_law/parsers/{file_path(module)}"),
        spider_path=String(f"public_law/spiders/{file_path(module)}"),
        tests_path=String(f"tests/public_law/parsers/{tests_path(module)}"),
        web_url=web_url,
    )


#
# At module load-time, we create the table and make it available
# in the public constant, `TABLE`.
#

# TODO: Figure out a way to automatically find these spider modules,
#       or the spider subclass each one contains.
from .spiders.aus import ip_glossary
from .spiders.can import doj_glossaries, parliamentary_glossary
from .spiders.int import rome_statute
from .spiders.irl import courts_glossary
from .spiders.nzl import justice_glossary
from .spiders.usa import georgia_ag_opinions, oregon_regs, us_courts_glossary

TABLE = MarkdownTable(
    (
        make_record(ip_glossary,            String("Australia/ip-glossary.json"),                     "https://www.public.law/dictionary/sources/ipaustralia.gov.au__tools-resources_ip-glossary"),
        make_record(courts_glossary,        String("Ireland/courts-glossary.json"),                   "https://www.public.law/dictionary/sources/courts.ie__glossary"),
        make_record(doj_glossaries,         String("Canada/doj-glossaries.json"),                     "https://www.public.law/dictionary/sources"),
        make_record(parliamentary_glossary, String("Canada/parliamentary-glossary.json"),             "https://www.public.law/dictionary/sources/lop.parl.ca__About_Parliament_Education_glossary-intermediate-students-e"),
        make_record(justice_glossary,       String("NewZealand/justice-glossary.json"),               "https://www.public.law/dictionary/sources/justice.govt.nz__about_glossary"),
        make_record(rome_statute,           String("Intergovernmental/RomeStatute/RomeStatute.json"), "https://world.public.law/rome_statute"),
        make_record(us_courts_glossary,     String("UnitedStates/us-courts-glossary.json"),           "https://www.public.law/dictionary/sources/uscourts.gov__glossary"),
        make_record_without_dataset(georgia_ag_opinions),
        make_record_without_dataset(oregon_regs, "https://oregon.public.law/rules"),
    )
)
