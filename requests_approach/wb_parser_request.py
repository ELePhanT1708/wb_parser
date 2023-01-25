import logging

import bs4
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb_parser')


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.0.0 Safari/537.36',
        }

    def load_page(self) -> str:
        url = 'https://www.wildberries.ru/catalog/knigi/uchebnaya-literatura#c115085312'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div')
        for block in container:
            self.parse_block(block)

    def parse_block(self, block):
        logger.info(block)
        logger.info('='* 100)

    def run(self):
        text = self.load_page()
        self.parse_page(text)

if __name__ == '__main__':
    parser = Client()
    parser.run()
