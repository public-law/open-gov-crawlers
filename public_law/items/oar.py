import scrapy

#
# Items for the Oregon Administrative Rules.
#


class OAR(scrapy.Item):
    chapters = scrapy.Field()
    date_accessed = scrapy.Field()


class Chapter(scrapy.Item):
    kind = scrapy.Field()
    db_id = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    divisions = scrapy.Field()


class Division(scrapy.Item):
    kind = scrapy.Field()
    db_id = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    rules = scrapy.Field()

    def number_in_rule_format(self) -> str:
        """Rules use zero-padded Division numbers"""
        number = self["number"] # type: ignore

        if isinstance(number, str):
            return number.zfill(3)
        else:
            raise ValueError(f"Division number is not a string: {self['number']}")


class Rule(scrapy.Item):
    kind = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    internal_url = scrapy.Field()

    authority = scrapy.Field()  # List[str]
    implements = scrapy.Field()  # List[str]
    history = scrapy.Field()  # str

    def division_number(self) -> str:
        number = self["number"] # type: ignore

        if isinstance(number, str):
            return number.split("-")[1]
        else:
            raise ValueError(f"Rule number is not a string: {self['number']}")
