import unittest

from scrapers.stocks import StockScraper

from bs4 import BeautifulSoup


class StockScraperTestCase(unittest.TestCase):

    TEST_STOCK = 'GOOG'

    def test_get_data(self):
        data = StockScraper().get_data(self.TEST_STOCK)
        self.assertIn(self.TEST_STOCK, data)

        stock = data[self.TEST_STOCK]
        keys = StockScraper.STOCK_KEYS[0] + StockScraper.STOCK_KEYS[1]

        for key in keys:
            self.assertIn(key, stock)
            self.assertIsNotNone(stock.get(key, None))


if __name__ == '__main__':
    unittest.main()
