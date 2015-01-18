import csv
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# STOCK_URL = 'http://finance.yahoo.com/q/?s={}'
# OPTIONS_URL = 'http://finance.yahoo.com/q/op?s={}'
# CONTRACT_KEYS = [
#     'strike',
#     'name',
#     'last',
#     'bid',
#     'ask',
#     'change',
#     '%change',
#     'volume',
#     'interest',
#     'volatility'
# ]
# STOCK_KEYS = [
#     [
#         'close',
#         'open',
#         'bid',
#         'ask',
#         '1y target',
#         'beta',
#         'earnings date',
#     ],
#     [
#         'day range',
#         '52wk range',
#         'volume',
#         '3m volume',
#         'cap',
#         'p/e',
#         'eps',
#         'div/yield'
#     ]
# ]


class BaseScraper(object):
    BASE_URL = None

    def __init__(self, ticker):
        self.ticker = ticker
        self.url = '{}?s={}'.format(self.BASE_URL, ticker)

    def _get_soup(self, url=None, html=None):
        if url:
            html = requests.get(url).content
        elif not html:
            html = requests.get(self.url).content
        return BeautifulSoup(str(html), 'lxml')

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

    # def __init__(self, ticker):
    #     super(OptionsScraper, self).__init__(ticker)

    @property
    def expiration_dates(self):
        if not self._expiration_dates:
            self._expiration_dates = self._get_expiration_dates()
        return self._expiration_dates

    def _get_expiration_dates(self):
        soup = self._get_soup()
        contract_list = soup.find('select', class_='Start-0')
        contract_soup = self._get_soup(html=contract_list)
        contract_names = contract_soup.find_all('option')
        contracts = {}
        for contract in contract_names:
            formatted_date = contract.text
            contracts[formatted_date] = contract['value']
        return contracts

    def _parse_table(self, table):
        contracts = []
        soup = self._get_soup(html=table.tbody)
        for row in soup.find_all('tr'):
            contract = {}
            cells = [x for x in row.contents if x != '\n']
            for i, cell in enumerate(cells):
                cell = self._get_soup(html=cell)
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

    def get_data(self):
        data = {}
        for date, query_param in self.expiration_dates.iteritems():
            data[date] = self._get_data_for_exp_date(query_param)
        return data








# def _get_soup(url):
#     html_page = requests.get(url).content
#     return BeautifulSoup(html_page, 'lxml')

# def _get_contract_query_params(ticker):
#     url = OPTIONS_URL.format(ticker)
#     soup = _get_soup(url)
#     contract_list = soup.find('select', class_='Start-0')
#     contract_soup = BeautifulSoup(str(contract_list), 'lxml')
#     contract_options_elements = contract_soup.find_all('option')
#     contracts = {}
#     for contract in contract_options_elements:
#         formatted_date = datetime.strptime(contract.text, '%B %d, %Y')
#         contracts[formatted_date] = contract['value']
#     return contracts

# def _get_particular_option_data(table):
#     contracts = []
#     soup = BeautifulSoup(str(table.tbody), 'lxml')
#     for row in soup.find_all('tr'):
#         contract_dict = {}
#         for i, cell in enumerate([x for x in row.contents if x != '\n']):
#             cell = BeautifulSoup(str(cell), 'lxml')
#             contract_dict[CONTRACT_KEYS[i]] = cell.text[1:-1]
#         contracts.append(contract_dict)
#     return contracts

# def _get_options_data_for_contract(ticker, contract):
#     url = '{}&date={}'.format(OPTIONS_URL.format(ticker), contract)
#     soup = _get_soup(url)
#     table = soup.find_all('table', class_='quote-table')
#     return {
#         'calls': _get_particular_option_data(table[0]),
#         'puts': _get_particular_option_data(table[1])
#     }


# def convert_to_csv(data, filename):
#     with open(filename, 'w+') as f:
#         writer = csv.writer(f)
#         writer.writerow(CONTRACT_KEYS)
#         for date in data:
#             writer.writerow([date])
#             contracts = data[date]
#             for call_or_put in contracts:
#                 writer.writerow([call_or_put])
#                 for contract in contracts[call_or_put]:
#                     writer.writerow([contract[col] for col in CONTRACT_KEYS])


# def _get_current_stock_price(soup):
#     return soup.find('span', class_='time_rtq_ticker').text

# def _parse_stock_data_table(soup):
#     stock_dict = {}
#     tables = [soup.find(id='table1'), soup.find(id='table2')]
#     for elem in zip(STOCK_KEYS, tables):
#         keys, table = elem
#         table = BeautifulSoup(str(table), 'lxml')
#         for i, cell in enumerate(table.find_all('td')):
#             stock_dict[keys[i]] = cell.text
#     return stock_dict

# def get_stock_data(ticker):
#     soup = _get_soup(STOCK_URL.format(ticker))
#     current_price = _get_current_stock_price(soup)
#     data = _parse_stock_data_table(soup)
#     data['ticker'] = ticker
#     data['current'] = current_price
#     return data

# def get_options_data(ticker, csv=False, csv_filename=None):
#     contracts = _get_contract_query_params(ticker)
#     data = {}
#     for date, name in contracts.iteritems():
#         data[date] = _get_options_data_for_contract(ticker, name)

#     if csv:
#         if not csv_filename:
#             csv_filename = '{}-options.csv'.format(ticker)
#         return convert_to_csv(data, csv_filename)

#     return data
