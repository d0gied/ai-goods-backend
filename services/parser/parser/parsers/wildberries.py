import datetime

import requests
from tqdm import tqdm

from ..models import Good
from .base import Parser


class WildberriesParser(Parser):
    """Wildberries parser"""

    def make_basket(self, e):  # NOTE do it prittier
        if 0 <= e <= 143:
            t = "01"
        elif 144 <= e <= 287:
            t = "02"
        elif 288 <= e <= 431:
            t = "03"
        elif 432 <= e <= 719:
            t = "04"
        elif 720 <= e <= 1007:
            t = "05"
        elif 1008 <= e <= 1061:
            t = "06"
        elif 1062 <= e <= 1169:
            t = "07"
        elif 1116 <= e <= 1169:
            t = "08"
        elif 1170 <= e <= 1313:
            t = "09"
        elif 1314 <= e <= 1601:
            t = "10"
        elif 1602 <= e <= 1655:
            t = "11"
        elif 1656 <= e <= 1919:
            t = "12"
        elif 1920 <= e <= 2045:
            t = "13"
        else:
            t = "14"
        return t

    def make_img(self, id):
        e = id // 100000
        basket = self.make_basket(e)
        img_url = f"https://basket-{basket}.wb.ru/vol{e}/part{id//1000}/{id}/images/big/1.webp"
        return img_url

    def get_response(self, search_name, sort, page):
        request = f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&page={page}&query=%{search_name}&resultset=catalog&sort={sort}&spp=29&suppressSpellcheck=false"
        response = requests.get(url=request)
        return response

    def make_card(self, response: dict, goods: list):
        card_list = response["data"]["products"]
        for card in card_list:
            id = card["id"]
            new_card = {
                "url": self.make_card_url(id),
                "price": int(card["salePriceU"] / 100),
                "name": card["name"],
                "rating": card["reviewRating"],
                "img": self.make_img(id),
                "reviews": card["feedbacks"],
            }
            goods.append(new_card)
        return goods

    def parse_by_name(self, search_name: str, sort: str, count_pages: int):
        goods = []

        for page in range(1, count_pages + 1):
            response = self.get_response(search_name, sort, page)
            if response.status_code == 200:
                goods = self.make_card(response.json(), goods)
            else:
                return goods

        return goods

    def parse_by_link(self, link: str):
        id = link.split("/")[4]
        request = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=28&nm={id}"

        response = requests.get(url=request)
        if response.status_code == 200:
            goods = self.make_card(response.json(), [])
            return goods
        else:
            return []

    def make_card_url(self, id):
        return f"https://www.wildberries.ru/catalog/{id}/detail.aspx"

    def check_goods(self, goods):
        if goods:
            return 200
        else:
            return 429

    def parse_request(self, search_request: str, sort: str, limit: int) -> list[dict]:
        """
        Парсит товары на WB, возвращает list[dict]
        """

        if sort not in ["popular", "priceup", "pricedown", "rate"]:
            sort = "popular"

        count_pages = (limit + 99) // 100

        if "wildberries.ru/catalog" in search_request:
            return self.parse_by_link(search_request)[:limit]
        else:
            return self.parse_by_name(search_request, sort, count_pages)[:limit]

    @staticmethod
    def json2good(data: dict) -> Good:
        return Good(
            id=data["url"].split("catalog/")[1].split("/")[0],
            name=data["name"],
            created_at=datetime.datetime.now(),
            price=data["price"],
            images=[data["img"]],
            source="wildberries",
            url=data["url"],
            rating=data["rating"],
            reviews=data["reviews"],
        )

    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        sort = kwargs.get("sort", "popular")
        data = self.parse_request([request], sort, limit)
        return [self.json2good(x) for x in data]  # NOTE kostyl

    def get_good(self, good_id: int, **kwargs) -> Good:
        ...
