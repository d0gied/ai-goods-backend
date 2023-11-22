import warnings

import selenium
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options


def test_selenium_connection():
    return warnings.warn("Not implemented")
    ua = UserAgent(browsers=["chrome"])

    options = Options()
    options.add_argument("--disable-3d-apis")
    options.add_argument("--headless=new")
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = selenium.webdriver.Chrome(options=options)
    driver.get("https://google.com")
    driver.quit()
