from sys import argv
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


def get_soup(url):
    html_page = requests.get(url).content
    return BeautifulSoup(html_page, 'lxml')

def get_contract_query_params(ticker):
    url = BASE_URL.format(ticker)
    soup = get_soup(url)
    contract_list = soup.find('select', class_='Start-0')
    contract_soup = BeautifulSoup(str(contract_list), 'lxml')
    contract_options_elements = contract_soup.find_all('option')
    contracts = {}
    for contract in contract_options_elements:
        date = contract.text
        formatted_date = datetime.strptime(date, '%B %d, %Y')
        contracts[formatted_date] = contract['value']
    return contracts

def get_particular_option_data(table):
    contracts = []
    soup = BeautifulSoup(str(table.tbody), 'lxml')
    table_rows = soup.find_all('tr')
    for row in table_rows:
        contract_dict = {}
        for i, cell in enumerate([x for x in row.contents if x != '\n']):
            cell = BeautifulSoup(str(cell), 'lxml')
            contract_dict[CONTRACT_KEYS[i]] = cell.text[1:-1]
        contracts.append(contract_dict)
    return contracts

def get_options_data_for_contract(ticker, contract):
    url = '{}&date={}'.format(BASE_URL.format(ticker), contract)
    soup = get_soup(url)
    table = soup.find_all('table', class_='quote-table')
    return {
        'calls': get_particular_option_data(table[0]),
        'puts': get_particular_option_data(table[1])
    }


def main():
    _, ticker = argv
    contracts = get_contract_query_params(ticker)
    data = {}
    for date, name in contracts.iteritems():
        data[date] = get_options_data_for_contract(ticker, name)
    return data


if __name__ == '__main__':
    main()
