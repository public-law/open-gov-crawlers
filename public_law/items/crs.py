from dataclasses import dataclass

#
# Items for the Colorado Revised Statutes.
#


@dataclass(frozen=True)
class Title:
    name: str
    number: str
    divisions: list
    source_url: str


@dataclass(frozen=True)
class Division:
    name: str
    source_url: str
    articles: list
