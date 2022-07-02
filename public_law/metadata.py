from dataclasses import dataclass, asdict
from datetime import date
from typing import Any, Literal

from public_law.dates import today
from public_law.text import NonemptyString


@dataclass(frozen=True)
class Metadata:  # pylint:disable=too-many-instance-attributes
    """Each JSON output file should have a `Metadata` object with the attributes:

    - `dc:creator`       An entity responsible for making the resource. Recommended practice is to identify the creator with a URI. If this is not possible or feasible, a literal value that identifies the creator may be provided.
    - `dc:identifier`    An unambiguous reference to the resource within a given context. Recommended practice is to identify the resource by means of a string conforming to an identification system. Examples include International Standard Book Number (ISBN), Digital Object Identifier (DOI), and Uniform Resource Name (URN). Persistent identifiers should be provided as HTTP URIs.
    - `dc:language`      An [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
    - `dc:publisher`     An entity responsible for making the resource available.
    - `dc:source`        The source URL. (A related resource from which the described resource is derived. This property is intended to be used with non-literal values. The described resource may be derived from the related resource in whole or in part. Best practice is to identify the related resource by means of a URI or a string conforming to a formal identification system.)
    - `dc:type`          Literal: "Dataset". (The nature or genre of the resource. Recommended practice is to use a controlled vocabulary such as the DCMI Type Vocabulary.)
    - `dc:title`         A name given to the resource.
    - `dcterms:format`   The file format, physical medium, or dimensions of the resource. Recommended practice is to use a controlled vocabulary such as the list of Internet Media Types.
    - `dcterms:license`  "https://creativecommons.org/licenses/by/4.0/"
    - `dcterms:modified` The date the resource was last modified. I.e., last accessed date.
    - `publiclaw:sourceModified` The date the original (gov't) source was last modified.

    See:

    * [Publishing Metadata](https://www.dublincore.org/resources/userguide/publishing_metadata/)
    * [Creating Metadata](https://www.dublincore.org/resources/userguide/creating_metadata/)
    * [Dublin Core Specs](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
    """

    dc_title: NonemptyString

    # URL of the original gov't document.
    dc_source: NonemptyString
    dc_language: Literal["de", "en", "fr"]

    # Jurisdiction.
    dcterms_coverage: NonemptyString
    publiclaw_sourceModified: date
    publiclaw_sourceCreator: NonemptyString

    dc_creator: str = "https://public.law"
    dc_type: str = "Dataset"
    dcterms_modified: date = today()
    dcterms_license: str = "https://creativecommons.org/licenses/by/4.0/"
    dcterms_format: str = "application/json"

    def as_dublin_core_dict(self) -> dict[str, Any]:
        """Return a dict containing the metadata with proper DublinCore
        naming syntax. Instead of keys such as `dc_title`, they should be
        in the form, `dc:title`."""

        return asdict(self, dict_factory=_make_dc_dict)

    def __iter__(self):
        return iter(self.as_dublin_core_dict().items())

    def __getitem__(self, k: str) -> Any:
        return self.as_dublin_core_dict().__getitem__(k)

    def __len__(self):
        return self.as_dublin_core_dict().__len__()

    def __repr__(self) -> str:
        return asdict(self).__repr__()


def _make_dc_dict(item_list: list[tuple[str, Any]]) -> dict[str, Any]:
    """Transform the keys in the items by converting underscores
    to colons."""
    return {k.replace("_", ":"): v for k, v in item_list}
