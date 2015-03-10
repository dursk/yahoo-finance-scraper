import unittest

from scrapers.stocks import StockScraper
from scrapers.options import OptionScraper

from bs4 import BeautifulSoup


TICKER = 'XON'


class StockScraperTestCase(unittest.TestCase):

    def test_get_data(self):
        data = StockScraper().get_data(TICKER)
        self.assertIn(TICKER, data)

        stock = data[TICKER]
        keys = StockScraper.STOCK_KEYS[0] + StockScraper.STOCK_KEYS[1]

        for key in keys:
            self.assertIn(key, stock)
            self.assertIsNotNone(stock.get(key, None))


class OptionScraperTestCase(unittest.TestCase):

    def test_get_data(self):
        data = OptionScraper().get_data(TICKER)

        underlying = data.pop('underlying')
        self.assertIsNot(underlying, '')

        for exp_date in data.values():
            for option in exp_date['calls'] + exp_date['puts']:
                for key in OptionScraper.CONTRACT_KEYS:
                    self.assertIn(key, option)


if __name__ == '__main__':
    unittest.main()
