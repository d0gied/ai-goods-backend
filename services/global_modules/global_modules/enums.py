from enum import Enum


class CeleryQueue(str, Enum):
    STORAGE = "storage"
    PARSE_WILDBERRIES: str = "parse.wildberries"
    PARSE_ALIBABA: str = "parse.alibaba"
    PARSE_OZON: str = "parse.ozon"
    SCRAPE: str = "scrape"
    ML_IMAGE: str = "ml.image"
    ML_NAME: str = "ml.name"
    ML_NAME_IMAGE: str = "ml.name_image"
