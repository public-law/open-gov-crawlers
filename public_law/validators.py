from schematics.models import Model
from schematics.types import URLType, StringType, ListType


class GlossaryEntry(Model):
    phrase: StringType(required=True)
    definition: StringType(required=True)


class Glossary(Model):
    source_url: URLType(required=True)
    name: StringType(required=True)
    author: StringType(required=True)
    pub_date: StringType(required=True)
    scrape_date: StringType(required=True)
    entries: ListType(GlossaryEntry)