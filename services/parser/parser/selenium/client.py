from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from ..config import SELENIUM_HOST


class SeleniumClient:
    def __init__(self, options: webdriver.ChromeOptions=None) -> None:
        if options == None:
            options = webdriver.ChromeOptions()
        self.options = options
        self.driver: WebDriver
    
    def __enter__(self):
        self.driver = webdriver.Remote(
            command_executor=SELENIUM_HOST, options=self.options
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

if __name__ == "__main__":
    with Client() as cl:
        cl.driver.get("google.com")
        print(cl.driver.title)