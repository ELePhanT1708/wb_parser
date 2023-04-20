import json
import os
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import logging

from selenium.webdriver.common.by import By

logging.basicConfig(filename='wb_parser.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.info("Loading started !!!!! ")
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

    def collect_single_book_page_urls_from_brand_page(self, url_for_all_books_of_one_brand: str, pages: int) -> List[
        str]:
        list_of_urls = []
        SCROLL_PAUSE_TIME = 0.1
        for i in range(1, pages):
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

        # print(list_of_urls)
        # print(len(list_of_urls))
        return list_of_urls

    def parse_book_page(self, book_url: str = 'srs', pause: int = 0):
        # self.driver.get("https://www.wildberries.ru/catalog/87623000/detail.aspx")
        self.driver.get(book_url)
        img_url_list = []
        characterisitcs = {}
        time.sleep(0.5)
        buttons_to_open = self.driver.find_elements(By.CSS_SELECTOR, ".collapsable .collapsible__toggle")
        # click on all "Развернуть описание и развернуть характеристики"
        for button in buttons_to_open:
            button.click()
        try:

            characteristics = self.driver.find_elements(By.CSS_SELECTOR,
                                                        ".product-page .product-params__cell-decor span")

            values = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .product-params__table td")
            price = self.driver.find_elements(By.CSS_SELECTOR, ".product-page .price-block__final-price")[0]
            description = self.driver.find_elements(By.CSS_SELECTOR, ".collapsable .collapsable__content")[1]
            brand = self.driver.find_elements(By.CLASS_NAME, "product-page__header")[0].find_elements(By.CLASS_NAME,
                                                                                                      "hide-mobile")[0]
            title = \
                self.driver.find_elements(By.CLASS_NAME, "product-page__header")[0].find_elements(By.CSS_SELECTOR,
                                                                                                  "h1")[0]
        except:
            pass

        for charast, value in zip(characteristics[5:], values[5:]):
            characterisitcs[f'{charast.text}'] = value.text
            # print(charast.text, ' - ', value.text)
        try:
            characterisitcs['Цена'] = price.text
            characterisitcs['Описание'] = description.text
            characterisitcs['Название'] = title.text
            characterisitcs['Бренд'] = brand.text
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
        # print(img_url_list)
        # print(characterisitcs)
        return {
            'pictures': img_url_list,
            'Charasteristics': characterisitcs
        }

    def collect_urls_for_brand(collector, url: str, pages: int, output_file: str):
        list_of_urls = collector.collect_single_book_page_urls_from_brand_page(url, pages)
        with open(output_file, "w", encoding='windows-1251') as outfile:
            for url in list_of_urls:
                outfile.write(url + '\n')

    def break_into_pieces(self, src_file: str):
        with open(src_file, 'r', encoding='windows-1251') as src_urls:
            rows = src_urls.readlines()
            quantity = len(rows)
            partition = int(quantity / 20)
            output_base_name = src_file.split('.')[0]


        for i in range(1, 21):
            path_to = f'{os.path.join(output_base_name + "_" + str(i) + ".txt")}'

            with open(f'{path_to}', 'w', encoding='windows-1251') as output:
                logger.info(f"{i}th partition was written !")
                output.writelines(rows[(i - 1) * partition: i * partition])
                # print(f"{i}th partition was written !")

    def parse_details_by_partition(self, urls_dir: str):
        files = os.listdir(urls_dir)
        for file in files:
            json_details = {}
            try:
                with open(os.path.join(urls_dir, file), 'r', encoding='windows-1251') as src:
                    for book_url in src:
                        book_url = book_url.strip()
                        res = self.parse_book_page(book_url)
                        json_details[f'{book_url}'] = res
                json_object = json.dumps(json_details, indent=4, ensure_ascii=False)
                with open(f"ПРОФСПЕЦТОРГ/details/{file.split('.')[0]}.json", "w", encoding='utf-8') as outfile:
                    outfile.write(json_object)
                logger.info(f'{file} was successfully parsed !  ')


            except Exception as e:
                logger.error(e)
                logger.error(f"{file} didn't work properly ")
                logger.exception(e)


if __name__ == '__main__':
    watcher = Watcher()
    brand_url = 'https://www.wildberries.ru/seller/260862'  # ссылка на селлера
    pages = 6  # количество товаров делишь 100 и прибавляешь 2 ( 465 товара -> 4 + 2 = 6 )
    # тут создаешь папку в проекте под названием селлера и пишешь сюда путь с расширением txt
    output_filename = 'ПРОФСПЕЦТОРГ/urls_partitions/ПРОФСПЕЦТОРГ_urls.txt'
    # собирает все ссылки на товары по селеру и пишет в txt
    watcher.collect_urls_for_brand(brand_url, pages, output_filename)
    # тут разбивает эти ссылки на 20 разных файлов чтобы если упадет не потерять все что было до
    watcher.break_into_pieces(output_filename)
    # следующую строку закомментируи сначала(перед первым запуском) и запусти все что выше в первый раз
    # во второй раз уже комментируи все что выше кроме первой строчки в мейне
    # но перед запуском все эти 20 файлов с сссылками на товары в отдельную папку и укажи полный путь до нее в функции
    # также нужно создать в папке селлера папку под названием "details" перед тем как запустить
    # и запускай
    watcher.parse_details_by_partition(
        r"C:\Users\Рамиль\PycharmProjects\wb_parser\selenuim_approach\ПРОФСПЕЦТОРГ\urls_partitions")

    # после того как все норм переходи в скрипт json_merge.py


    # если че то сломалось , есть лог файл он называется wb_parser.log
    # там будет написано на каком файле все сломалось и если порыться в коде то можно будет разобраться где нужно поменять
    # чтоб не делать все заново
    # пока я сам не понял где это надо сделать
    # но будем надеяться что ломаться не будет

