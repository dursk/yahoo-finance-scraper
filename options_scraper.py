import csv
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from data import RAW_HTML_1
from data2 import RAW_HTML_2


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
    # url = '{}&date={}'.format(BASE_URL.format(ticker), contract)
    # soup = _get_soup(url)
    soup = BeautifulSoup(contract, 'lxml')
    table = soup.find_all('table', class_='quote-table')
    return {
        'calls': _get_particular_option_data(table[0]),
        'puts': _get_particular_option_data(table[1])
    }


def convert_to_csv(data, filename):
    with open(filename, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(CONTRACT_KEYS)
        for date in data:
            writer.writerow([date])
            contracts = data[date]
            for call_or_put in contracts:
                writer.writerow([call_or_put])
                for contract in contracts[call_or_put]:
                    writer.writerow([contract[col] for col in CONTRACT_KEYS])


def get_options_data(ticker, csv=False, csv_filename=None):
    # contracts = _get_contract_query_params(ticker)
    contracts = {
        datetime.min: RAW_HTML_1,
        datetime.max: RAW_HTML_2
    }
    data = {}
    for date, name in contracts.iteritems():
        data[date] = _get_options_data_for_contract(ticker, name)

    if csv:
        if not csv_filename:
            csv_filename = '{}-options.csv'.format(ticker)
        return convert_to_csv(data, csv_filename)

    return data
