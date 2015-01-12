from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://finance.yahoo.com/q/op?s={}'
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


def _get_soup(url):
    html_page = requests.get(url).content
    return BeautifulSoup(html_page, 'lxml')

def _get_contract_query_params(ticker):
    url = BASE_URL.format(ticker)
    soup = _get_soup(url)
    contract_list = soup.find('select', class_='Start-0')
    contract_soup = BeautifulSoup(str(contract_list), 'lxml')
    contract_options_elements = contract_soup.find_all('option')
    contracts = {}
    for contract in contract_options_elements:
        formatted_date = datetime.strptime(contract.text, '%B %d, %Y')
        contracts[formatted_date] = contract['value']
    return contracts

def _get_particular_option_data(table):
    contracts = []
    soup = BeautifulSoup(str(table.tbody), 'lxml')
    for row in soup.find_all('tr'):
        contract_dict = {}
        for i, cell in enumerate([x for x in row.contents if x != '\n']):
            cell = BeautifulSoup(str(cell), 'lxml')
            contract_dict[CONTRACT_KEYS[i]] = cell.text[1:-1]
        contracts.append(contract_dict)
    return contracts

def _get_options_data_for_contract(ticker, contract):
    url = '{}&date={}'.format(BASE_URL.format(ticker), contract)
    soup = _get_soup(url)
    table = soup.find_all('table', class_='quote-table')
    return {
        'calls': _get_particular_option_data(table[0]),
        'puts': _get_particular_option_data(table[1])
    }


def get_options_data(ticker):
    contracts = _get_contract_query_params(ticker)
    data = {}
    for date, name in contracts.iteritems():
        data[date] = _get_options_data_for_contract(ticker, name)
    return data
