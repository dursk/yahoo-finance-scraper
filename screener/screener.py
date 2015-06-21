import csv

from bs4 import BeautifulSoup
import requests


URL = 'http://screener.finance.yahoo.com/b'


def search(params):
    if 'vw' not in params:
        params['vw'] = 0
    params['db'] = 'stocks'
    html = requests.get(URL, params=params).content
    soup = BeautifulSoup(str(html), 'lxml')
    table_attrs = {
        'border': 1,
        'cellpadding': 2,
        'cellspacing': 0,
        'width': '100%'
    }
    data_table = soup.find('table', attrs=table_attrs)
    _write_to_csv(data_table)

def _parse_table(data_table):
    for row in data_table.find_all('tr'):
        parsed_row = []
        for cell in row.find_all('td'):
            parsed_row.append(unicode(cell.text).encode('utf-8'))
        yield parsed_row

def _write_to_csv(data_table):
    with open('screener_data.csv', 'w') as f:
        writer = csv.writer(f)
        for row in _parse_table(data_table):
            writer.writerow(row)
