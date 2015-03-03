import csv

from base_scraper import BaseScraper


class StockScraper(BaseScraper):
    STOCK_KEYS = [
        [
            'close',
            'open',
            'bid',
            'ask',
            '1y target',
            'beta',
            'earnings date'
        ],
        [
            'day range',
            '52wk range',
            'volume',
            '3m volume',
            'cap',
            'p/e',
            'eps',
            'div/yield'
        ]
    ]
    BASE_URL = 'http://finance.yahoo.com/q'

    def _parse_table(self, soup):
        stock = {}
        tables = [soup.find(id='table1'), soup.find(id='table2')]
        for elem in zip(self.STOCK_KEYS, tables):
            keys, table = elem
            table = self._convert_to_soup(table)
            for i, cell in enumerate(table.find_all('td')):
                stock[keys[i]] = cell.text
        return stock

    def _write_csv_headers(self, writer):
        header_row = ['ticker', 'current']
        for sub_list in self.STOCK_KEYS:
            header_row.extend(sub_list)
        writer.writerow(header_row)

    def _write_csv_data_rows(self, writer, tickers):
        data = self.get_data(tickers)
        for ticker in data:
            ticker_data = data[ticker]
            row = [ticker, ticker_data['current']]
            for sub_list in self.STOCK_KEYS:
                row.extend([ticker_data[i] for i in sub_list])
            writer.writerow(row)

    def _get_current_price(self, soup):
        return soup.find('span', class_='time_rtq_ticker').text

    def get_data(self, tickers):
        if type(tickers) is str:
            tickers = [tickers]
        data = {}
        for ticker in tickers:
            url = self._get_url(ticker)
            soup = self._get_soup(url)
            ticker_data = self._parse_table(soup)
            ticker_data['current'] = self._get_current_price(soup)
            data[ticker] = ticker_data
        return data

    def export_to_csv(self, tickers, filename=None):
        if type(tickers) is str:
            tickers = [tickers]
        if not filename:
            filename = 'stock_data.csv'
        with open(filename, 'w+') as f:
            writer = csv.writer(f)
            self._write_csv_headers(writer)
            self._write_csv_data_rows(writer, tickers)
