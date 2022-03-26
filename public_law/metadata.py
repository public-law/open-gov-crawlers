from dataclasses import dataclass
from public_law.text import NonemptyString
from public_law.dates import todays_date


@dataclass(frozen=True)
class Metadata:
    """Each JSON output file should have a `Metadata` object with the attributes:

    - `dc:creator`
    - `dc:identifier`
    - `dc:language`
    - `dc:publisher`
    - `dc:source`
    - `dc:type`
    - `dc:title`
    - `dcterms:license`
    - `dcterms:modified`

    See:

    * [Publishing Metadata](https://www.dublincore.org/resources/userguide/publishing_metadata/)
    * [Creating Metadata](https://www.dublincore.org/resources/userguide/creating_metadata/)
    * [Dublin Core Specifications](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
    """

    dc_creator: NonemptyString
    dc_identifier: NonemptyString
    dc_language: NonemptyString
    dc_source: NonemptyString
    dc_title: NonemptyString

    dc_publisher: str = "Public.Law"
    dc_type: str = "text"
    dcterms_license: str = "BY"
    dcterms_modified: str = todays_date()