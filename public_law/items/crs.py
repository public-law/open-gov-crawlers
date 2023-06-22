from dataclasses import dataclass

#
# Items for the Colorado Revised Statutes.
#


@dataclass(frozen=True)
class Article:
    """A CRS Article."""

    name: str
    number: str
    source_url: str


@dataclass(frozen=True)
class Division:
    """A CRS Division."""

    name: str
    source_url: str
    articles: list[Article]


@dataclass(frozen=True)
class Title:
    """A CRS Title."""

    name: str
    number: str
    source_url: str
    divisions: list[Division]
