from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import logging

from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb_parser')

WINDOW_SIZE = "1920,1080"


class Watcher:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.service = Service('"C:\\Users\\Рамиль\\PycharmProjects\\wb_parser\\selenuim_approach\\chromedriver.exe"')
        # for ChromeDriver version 79.0.3945.16 or over
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        # self.options.add_argument("--headless")
        # self.options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # user-agent
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )

    def collect_single_book_page_urls_from_brand_page(self, url_for_all_books_of_one_brand: str) -> List[str]:
        self.driver.get(url=url_for_all_books_of_one_brand)
        list_of_urls = []
        books_on_page = self.driver.find_elements(By.CSS_SELECTOR, 'img.j-thumbnail.thumbnail')
        print(books_on_page)
        for book in books_on_page:
            url = book.get_attribute('href')
            print(url)

    def parse_book_page(self, pause: int = 0):
        # self.driver.get("https://www.wildberries.ru/catalog/115085312/detail.aspx")
        self.driver.get("https://www.wildberries.ru/catalog/102479872/detail.aspx")
        time.sleep(pause)
        buttons_to_open = self.driver.find_elements(By.CSS_SELECTOR, ".collapsable .collapsible__toggle")
        # click on all "Развернуть описание и развернуть характеристики"
        for button in buttons_to_open:
            button.click()
        characteristics = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .product-params__cell-decor span")
        values = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .product-params__table td")
        for charast, value in zip(characteristics[5:], values[5:]):
            print(charast.text, ' - ', value.text)

        images = self.driver.find_elements(By.CSS_SELECTOR, "div.slide__content.img-plug.j-wba-card-item")
        for img in images:
            url = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
            print(url)


# class Client:
#     def __init__(self):
#         self.session = requests.Session()
#         self.session.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/109.0.0.0 Safari/537.36',
#         }
#
#     def load_page(self) -> str:
#         url = 'https://www.wildberries.ru/catalog/knigi/uchebnaya-literatura#c115085312'
#         res = self.session.get(url=url)
#         res.raise_for_status()
#         return res.text
#
#     def parse_page(self, text: str):
#         soup = bs4.BeautifulSoup(text, 'lxml')
#         container = soup.select('div')
#         for block in container:
#             self.parse_block(block)
#
#     def parse_block(self, block):
#         logger.info(block)
#         logger.info('='* 100)
#
#     def run(self):
#         text = self.load_page()
#         self.parse_page(text)

if __name__ == '__main__':
    watcher = Watcher()
    watcher.collect_single_book_page_urls_from_brand_page('https://www.wildberries.ru/brands/rostkniga/all')
