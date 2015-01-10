from datetime import datetime
from sys import argv

import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://finance.yahoo.com/q/op?s={}'

def main():
    _, ticker = argv
    html = requests.get(BASE_URL.format(ticker)).content
    main_soup = BeautifulSoup(html, 'lxml')
    contract_list = main_soup.find_all('select', class_='Start-0')
    contract_soup = BeautifulSoup(str(contract_list), 'lxml')
    contract_options_elements = contract_soup.find_all('option')
    contract_dates = {}
    for contract in contract_options_elements:
        date = contract.text
        formatted_date = datetime.strptime(date, '%B %d, %Y')
        contract_dates[formatted_date] = contract['value']
    print contract_dates

if __name__ == '__main__':
    main()
