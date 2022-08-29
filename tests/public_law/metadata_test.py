from typing import Any
from public_law.metadata import Metadata, Subject
from public_law.text import URI, NonemptyString as S
from public_law.dates import today

import pytest


@pytest.fixture
def simple_input() -> Metadata:
    return Metadata(
        dcterms_source=S("https://a.b.c"),
        dcterms_title=S("The Title"),
        dcterms_language="en",
        dcterms_modified=today(),
        dcterms_coverage="CAN",
        dcterms_subject=(
            Subject(URI("http://id.loc/1234"), S("taxation")),
            Subject(URI("http://id.wiki"), S("taxes")),
        ),
        publiclaw_sourceModified=today(),
        publiclaw_sourceCreator=S("Some Canadian Agency"),
    )


@pytest.fixture
def simple_output() -> dict[str, Any]:
    return {
        "dcterms:creator": "https://public.law",
        "dcterms:language": "en",
        "dcterms:source": "https://a.b.c",
        "dcterms:title": "The Title",
        "dcterms:type": "Dataset",
        "dcterms:coverage": "CAN",
        "dcterms:format": "application/json",
        "dcterms:license": "https://creativecommons.org/licenses/by/4.0/",
        "dcterms:modified": today(),
        "dcterms:subject": (
            {
                "uri": "http://id.loc/1234",
                "rdfs:label": "taxation",
            },
            {"uri": "http://id.wiki", "rdfs:label": "taxes"},
        ),
        "publiclaw:sourceModified": today(),
        "publiclaw:sourceCreator": "Some Canadian Agency",
        "publiclaw:readingEase": "unknown",
    }


def it_creates_a_dict_directly(simple_input, simple_output): # type: ignore
    generated_dict = simple_input.as_dublin_core_dict() # type: ignore

    assert generated_dict == simple_output


def it_creates_a_dict_via_core_func(simple_input, simple_output): # type: ignore
    generated_dict = dict(simple_input) # type: ignore

    assert generated_dict == simple_output
