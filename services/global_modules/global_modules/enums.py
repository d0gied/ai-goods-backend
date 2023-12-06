from enum import Enum

class CeleryQueue(Enum):
    STORAGE = 'storage'
    PARSE_WILDBERRIES = 'parse.wildberries'
    PARSE_ALIBABA = 'parse.alibaba'
    PARSE_OZON = 'parse.ozon'
    SCRAPE = 'scrape'