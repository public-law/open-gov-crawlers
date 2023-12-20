from typing import Callable
from toolz.functoolz import curry
from scrapy.http.response.xml import XmlResponse

from .selector_util import xpath_get


xpath_get = curry(xpath_get)
