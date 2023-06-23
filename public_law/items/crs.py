from dataclasses import dataclass

from public_law.text import NonemptyString, URL

#
# Items for the Colorado Revised Statutes.
#

@dataclass(frozen=True)
class Section:
    """A CRS Section.
    
    A typical section number looks like this:
        "16-1-101".

    It means:
        Title 16, Article 1, Maybe Part 1, Section 101.
    """
    name: NonemptyString
    number: NonemptyString
    source_url: URL
    text: NonemptyString


@dataclass(frozen=True)
class Part:
    """CRS Part: a nonstructural namespace level."""
    name: NonemptyString
    source_url: URL
    sections: list[Section]


@dataclass(frozen=True)
class Article:
    """A CRS Article."""
    name: NonemptyString
    number: NonemptyString
    source_url: URL
    sections: list[Section]


@dataclass(frozen=True)
class Division:
    """CRS Division: a nonstructural namespace level.

    Some titles have Divisions, others don't.
    """
    name: NonemptyString
    source_url: URL
    articles: list[Article]


@dataclass(frozen=True)
class Title:
    """A CRS Title."""
    name: NonemptyString
    number: NonemptyString
    source_url: URL
    children: list[Division] | list[Article]
