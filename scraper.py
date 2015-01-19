import csv
from exceptions import NotImplementedError

import requests
from bs4 import BeautifulSoup


class BaseScraper(object):
    BASE_URL = None

    def __init__(self, ticker):
        self.ticker = ticker
        self.url = '{}?s={}'.format(self.BASE_URL, ticker)

    def _get_soup(self, url):
        html = requests.get(url).content
        return BeautifulSoup(html, 'lxml')

    def _convert_to_soup(self, html):
        return BeautifulSoup(str(html), 'lxml')

    def get_data(self):
        raise NotImplementedError


class StockScraper(BaseScraper):
    STOCK_KEYS = [
        [
            'close',
            'open',
            'bid',
            'ask',
            '1y target',
            'beta',
            'earnings date',
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
        header_row = ['current']
        for sub_list in self.STOCK_KEYS:
            header_row.extend(sub_list)
        writer.writerow(header_row)

    def _write_csv_data_row(self, writer):
        data = self.get_data()
        row = [data['current']]
        for sub_list in self.STOCK_KEYS:
            row.extend([data[i] for i in sub_list])
        writer.writerow(row)

    def get_current_price(self, soup=None):
        if not soup:
            soup = self._get_soup(self.url)
        return soup.find('span', class_='time_rtq_ticker').text

    def get_data(self):
        soup = self._get_soup(self.url)
        data = self._parse_table(soup)
        data['ticker'] = self.ticker
        data['current'] = self.get_current_price(soup)
        return data

    def export_to_csv(self, filename=None):
        if not filename:
            filename = '{}.csv'.format(self.ticker)
        with open(filename, 'w+') as f:
            writer = csv.writer(f)
            self._write_csv_headers(writer)
            self._write_csv_data_row(writer)


class OptionsScraper(BaseScraper):
    CALL_INDEX = 0
    PUT_INDEX = 1
    CONTRACT_KEYS = [
        'strike',
        'name',
        'last',
        'bid',
        'ask',
        'change',
        '%change',
        'volume',
        'interest',
        'volatility'
    ]
    BASE_URL = 'http://finance.yahoo.com/q/op'
    _expiration_dates = None

    @property
    def expiration_dates(self):
        if not self._expiration_dates:
            self._expiration_dates = self._get_expiration_dates()
        return self._expiration_dates

    def _get_expiration_dates(self):
        soup = self._get_soup(self.url)
        contract_list = soup.find('select', class_='Start-0')
        contract_soup = self._convert_to_soup(contract_list)
        contract_names = contract_soup.find_all('option')
        contracts = {}
        for contract in contract_names:
            formatted_date = contract.text
            contracts[formatted_date] = contract['value']
        return contracts

    def _parse_table(self, table):
        contracts = []
        soup = self._convert_to_soup(table.tbody)
        for row in soup.find_all('tr'):
            contract = {}
            cells = [x for x in row.contents if x != '\n']
            for i, cell in enumerate(cells):
                cell = self._convert_to_soup(cell)
                contract[self.CONTRACT_KEYS[i]] = cell.text[1:-1]
            contracts.append(contract)
        return contracts

    def _get_data_for_exp_date(self, query_param):
        soup = self._get_soup('{}&date={}'.format(self.url, query_param))
        table = soup.find_all('table', class_='quote-table')
        return {
            'calls': self._parse_table(table[self.CALL_INDEX]),
            'puts': self._parse_table(table[self.PUT_INDEX])
        }

    def _write_all_data_to_csv(self, writer):
        writer.writerow(['Underlying:', options.pop('underlying')])
        writer.writerow(self.CONTRACT_KEYS)
        options = self.get_data()
        for date in options:
            writer.writerow([date])
            contracts = options[date]
            for option_type in contracts:
                writer.writerow([option_type])
                for contract in contracts[option_type]:
                    writer.writerow(
                        [contract[key] for key in self.CONTRACT_KEYS]
                    )

    def get_data(self):
        data = {}
        for date, query_param in self.expiration_dates.iteritems():
            data[date] = self._get_data_for_exp_date(query_param)
        data['underlying'] = StockScraper(self.ticker).get_current_price()
        return data

    def export_to_csv(self, filename=None):
        if not filename:
            filename = '{}options.csv'.format(self.ticker)
        with open(filename, 'w+') as f:
            writer = csv.writer(f)
            self._write_all_data_to_csv(writer)
