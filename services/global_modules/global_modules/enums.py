from enum import Enum


class CeleryQueue(Enum):
    STORAGE = "storage"
    PARSE_WILDBERRIES = "parse.wildberries"
    PARSE_ALIBABA = "parse.alibaba"
    PARSE_OZON = "parse.ozon"
    SCRAPE = "scrape"
    ML_IMAGE = "ml.image"
    ML_NAME = "ml.name"
    ML_NAME_IMAGE = "ml.name_image"
