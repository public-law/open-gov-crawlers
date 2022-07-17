# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false

from pprint import PrettyPrinter
from typing import Any
from public_law.metadata import Metadata
from public_law.text import NonemptyString as S
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
        "dcterms:subject": tuple(),
        "publiclaw:sourceModified": today(),
        "publiclaw:sourceCreator": "Some Canadian Agency",
        "publiclaw:readingEase": "unknown",
    }


def it_creates_a_dict_directly(simple_input, simple_output):
    generated_dict = simple_input.as_dublin_core_dict()

    assert generated_dict == simple_output


def it_creates_a_dict_via_core_func(simple_input, simple_output):
    generated_dict = dict(simple_input)

    assert generated_dict == simple_output
