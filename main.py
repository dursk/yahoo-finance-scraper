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

def main():
    _, ticker = argv
    url = BASE_URL.format(ticker)
    html = requests.get(url).content
    main_soup = BeautifulSoup(html, 'lxml')
    contract_list = main_soup.find('select', class_='Start-0')
    contract_soup = BeautifulSoup(str(contract_list), 'lxml')
    contract_options_elements = contract_soup.find_all('option')
    contracts = {}
    for contract in contract_options_elements:
        date = contract.text
        formatted_date = datetime.strptime(date, '%B %d, %Y')
        contracts[formatted_date] = contract['value']

    table = main_soup.find_all('table', class_='quote-table')
    call_table = table[0]
    put_table = table[1]

    put_contracts = []

    put_table_soup = BeautifulSoup(str(put_table.tbody), 'lxml')
    table_rows = put_table_soup.find_all('tr')

    for row in table_rows:
        contract_dict = {}

        for i, cell in enumerate([x for x in row.contents if x != '\n']):
            cell = BeautifulSoup(str(cell), 'lxml')
            contract_dict[CONTRACT_KEYS[i]] = cell.text[1:-1]

        put_contracts.append(contract_dict)

    call_contracts = []

    call_table_soup = BeautifulSoup(str(call_table.tbody), 'lxml')
    table_rows = call_table_soup.find_all('tr')

    for row in table_rows:
        contract_dict = {}

        for i, cell in enumerate([x for x in row.contents if x != '\n']):
            cell = BeautifulSoup(str(cell), 'lxml')
            contract_dict[CONTRACT_KEYS[i]] = cell.text[1:-1]

        call_contracts.append(contract_dict)

    return {'calls': call_contracts, 'puts': put_contracts}


if __name__ == '__main__':
    main()
