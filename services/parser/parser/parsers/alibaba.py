from .base import Parser
from ..models import Good
import math
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm
import datetime

class AlibabaParser(Parser):
    """Alibaba parser"""
    def __init__(self):
        self.data = dict()

    def get_options(self):
        ua = UserAgent(browsers=["chrome"])
        options = Options()
        options.add_argument("--disable-3d-apis")
        options.add_argument("--headless=new")
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument("--window-size=3440,1440")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        # options.add_argument("--blink-settings=imagesEnabled=false")
        # options.add_argument("--disable-infobars")
        # options.page_load_strategy = 'eager'

        # options.add_argument("--headless")
        # options.add_argument("--blink-settings=imagesEnabled=false")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-popup-blocking")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--ignore-certificate-errors")

        return options

    def get_img(self, a):
        return a.find_element(By.TAG_NAME, "img").get_attribute("src")

    def get_url(self, a):
        return a.get_attribute("href")

    def get_price(self, good):
        return float(
            good.find_element(By.CLASS_NAME, "search-card-e-price-main")
            .text.split(" - ")[-1]
            .replace(",", "")[1:]
        )

    def get_name(self, good):
        return good.find_element(By.CLASS_NAME, "search-card-e-title").text

    def get_feedbacks(self, good):
        try:
            feedbacks = good.find_element(By.CLASS_NAME, "search-card-e-review").text
            return float(feedbacks[:3]), int(feedbacks.split(" ")[-1][1:-1])
        except:
            return 0, 0

    def parse_pages(self, search_name, i, category):
        dr = webdriver.Chrome(options=self.get_options())
        print(
            f"https://www.alibaba.com/trade/search?spm=a2700.product_home_newuser.home_new_user_first_screen_fy23_pc_search_bar.recommendItem_pos_0&tab=all&searchText={search_name}&page={i+1}"
        )
        dr.get(
            f"https://www.alibaba.com/trade/search?spm=a2700.product_home_newuser.home_new_user_first_screen_fy23_pc_search_bar.recommendItem_pos_0&tab=all&searchText={search_name}&page={i+1}"
        )

        div_goods = dr.find_element(By.CLASS_NAME, "organic-list").find_elements(
            By.XPATH, "./div"
        )
        div_goods = [
            i
            for i in div_goods
            if i.get_attribute("class")
            != "organic-gallery-offer-outter J-offer-wrapper"
            and i.get_attribute("class") != "organic-gallery-offer-outter"
            and i.get_attribute("class") != "organic-list-offer-outter"
        ]

        for good in div_goods:
            a = good.find_element(By.CLASS_NAME, "search-card-e-slider__link")
            rate, feedback = self.get_feedbacks(good)

            params = {
                "img": self.get_img(a),
                "url": self.get_url(a),
                "rate": rate,
                "feedback": feedback,
                "price": self.get_price(good),
                "name": self.get_name(good),
            }
            category.append(params)
        dr.close()
        return category

    def parse_category(self, search_name, count):
        category = []

        count_pages = math.ceil(count / 47)

        for i in range(0, count_pages):
            print(i, count_pages)
            category = self.parse_pages(search_name, i, category)
        return {"status": 200, "search_name": search_name, "data": category}

    def parse_categories(self, search_names, count):
        categoties = []
        for name in tqdm(search_names):
            category = self.parse_category(name, count)
            categoties.append(category)

        new_data = {}
        for x in categoties:
            new_data[x["search_name"]] = x["data"]
        return new_data

    def make_data(self, categories):
        count = 200
        data = self.parse_categories(categories, count)

        for k, values in data.items():
            if k not in self.data:
                self.data[k] = values

    @staticmethod
    def json2good(data: dict) -> Good:
        return Good(
            id=data["url"].split("catalog/")[1].split("/")[0],
            name=data["name"],
            created_at=datetime.datetime.now(),
            price=data["price"],
            images=[data["img"]],
            source="alibaba",
            url=data["url"],
            rating=data["rating"],
            reviews=data["reviews"],
        )
    
    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        if request not in self.data:
            self.make_data([request])
        return self.data[request]
        # TODO: Implement this method
        raise NotImplementedError

    def get_good(self, good_id: str, **kwargs) -> Good:
        # TODO: Implement this method
        raise NotImplementedError