import csv

from bs4 import BeautifulSoup
import requests


URL = 'http://screener.finance.yahoo.com/b'


def get_csv(params):
    if 'vw' not in params:
        params['vw'] = 0
    params['b'] = 1
    params['db'] = 'stocks'

    with open('screener_data.csv', 'w') as f:
        writer = csv.writer(f)
        while True:
            html = requests.get(URL, params=params).content
            soup = BeautifulSoup(str(html), 'lxml')
            table_attrs = {
                'border': 1,
                'cellpadding': 2,
                'cellspacing': 0,
                'width': '100%'
            }
            data_table = soup.find('table', attrs=table_attrs)
            print data_table
            print '\n'
            if not data_table:
                break
            for row in _parse_table(data_table, first=(params['b'] == 1)):
                writer.writerow(row)
            params['b'] += 20

def _parse_table(data_table, first=False):
    rows = data_table.find_all('tr')
    if not first:
        rows.pop(0)
    for row in data_table.find_all('tr'):
        parsed_row = []
        for cell in row.find_all('td'):
            parsed_row.append(unicode(cell.text).encode('utf-8'))
        yield parsed_row
