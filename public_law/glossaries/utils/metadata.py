from public_law.shared.models.metadata import Metadata, Subject
from public_law.shared.utils.text import (
    LoCSubject,
    NonemptyString as String,
    URL,
)

def us_courts_glossary_metadata() -> Metadata:
    """
    Returns static metadata about the US Courts glossary source.
    """
    return Metadata(
        dcterms_title=String("Glossary of Legal Terms"),
        dcterms_language="en",
        dcterms_coverage="USA",
        # Info about original source
        dcterms_source=String("https://www.uscourts.gov/glossary"),
        publiclaw_sourceModified="unknown",
        publiclaw_sourceCreator=String("United States Courts"),
        dcterms_subject=(
            Subject(
                uri=LoCSubject("sh85033575"),
                rdfs_label=String("Courts--United States"),
            ),
            Subject(
                uri=URL("https://www.wikidata.org/wiki/Q194907"),
                rdfs_label=String("United States federal courts"),
            ),
        ),
    ) 
