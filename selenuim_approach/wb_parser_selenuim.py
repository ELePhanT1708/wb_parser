import json
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
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        # self.options.add_argument("--headless")
        # self.options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # user-agent
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/109.0.0.0 Safari/537.36")
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
          '''
        })

    def collect_single_book_page_urls_from_brand_page(self, url_for_all_books_of_one_brand: str) -> List[str]:
        list_of_urls = []
        SCROLL_PAUSE_TIME = 0.1
        for i in range(1, 11):
            # количество страниц товаров у бренда нужно глянуть самостоятельно
            # либо разделить количество товаров на сто и прибавить один к целой части

            self.driver.get(url=url_for_all_books_of_one_brand + f'?&page={i}&all=')

            time.sleep(2)


            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            last_height = 200
            next_height = 400

            for i in range(60):
                # Scroll down to bottom

                self.driver.execute_script(f"window.scrollTo({last_height}, {next_height});")
                last_height = next_height
                next_height += 200
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # # Calculate new scroll height and compare with last scroll height
                # new_height = self.driver.execute_script("return document.body.scrollHeight")
                # if new_height == last_height:
                #     break
                # last_height = new_height
            # books_on_page = self.driver.find_elements(By.CSS_SELECTOR, '.product-card')
            # books_on_page = self.driver.find_elements(By.CLASS_NAME, 'product-card__wrapper')
            # books_on_page = self.driver.find_elements(by=B)
            books_on_page = self.driver.find_elements(By.XPATH, "//div/a")
            # books_on_page = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "https://www.wildberries.ru/catalog/")
            length = len(books_on_page)
            for book in books_on_page:
                url = book.get_attribute('href')
                if 'catalog' in url:
                    list_of_urls.append(url)

        print(list_of_urls)
        print(len(list_of_urls))
        return list_of_urls

    def parse_book_page(self, book_url: str = 'srs', pause: int = 0):
        # self.driver.get("https://www.wildberries.ru/catalog/115085312/detail.aspx")
        self.driver.get(book_url)
        img_url_list = []
        characterisitcs = {}
        time.sleep(0.5)
        buttons_to_open = self.driver.find_elements(By.CSS_SELECTOR, ".collapsable .collapsible__toggle")
        # click on all "Развернуть описание и развернуть характеристики"
        for button in buttons_to_open:
            button.click()
        try:
            characteristics = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .product-params__cell-decor span")
            values = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .product-params__table td")
            price = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .price-block__final-price")[0]
            description = self.driver.find_elements(By.CSS_SELECTOR, ".collapsable .collapsable__content")[1]
        except:
            pass


        for charast, value in zip(characteristics[5:], values[5:]):
            characterisitcs[f'{charast.text}'] = value.text
            print(charast.text, ' - ', value.text)
        try:
            characterisitcs['Цена'] = int(price.text.split()[0])
            characterisitcs['Описание'] = description.text
        except:
            pass
        images = self.driver.find_elements(By.CSS_SELECTOR, "div.slide__content.img-plug.j-wba-card-item")
        video = self.driver.find_elements(By.CSS_SELECTOR, "div.slide__content.img-plug.j-wba-card-item play")

        for img in images:
            try:
                url = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                img_url_list.append(url)
            except:
                pass
        print(img_url_list)
        print(characterisitcs)
        return {
            'pictures': img_url_list,
            'Charasteristics': characterisitcs
        }



if __name__ == '__main__':
    watcher = Watcher()
    brand_url = 'https://www.wildberries.ru/seller/151127'
    # list_of_urls = watcher.collect_single_book_page_urls_from_brand_page(brand_url)
    # with open("z_book_urls.txt", "w", encoding='windows-1251') as outfile:
    #     for url in list_of_urls:
    #         outfile.write(url + '\n')
    json_info = {}
    with open("z_book_urls.txt", "r", encoding='windows-1251') as outfile:
        for row in outfile:
            res = watcher.parse_book_page(row)
            json_info[f'{row}'] = res
    # with open("rostkniga_all.txt", "w", encoding='windows-1251') as outfile:
    #     for url in list_of_urls:
    #         outfile.write(url + '\n')
    # with open("rostkniga_test.txt", "w", encoding='windows-1251') as outfile:
    #     for url in list_of_urls:
    #         outfile.write(url + '\n')
    # json_info = {}
    # for book in list_of_urls:
    #     res = watcher.parse_book_page(book)
    #     json_info[f'{book}'] = res
    # Serializing json
    json_object = json.dumps(json_info, indent=4, ensure_ascii=False)
    #
    # Writing to sample.json
    with open("z_book.json", "w", encoding='windows-1251') as outfile:
        outfile.write(json_object)

