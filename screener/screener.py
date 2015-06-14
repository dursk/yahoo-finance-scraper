import csv

from bs4 import BeautifulSoup
import requests


URL = 'http://screener.finance.yahoo.com/b'


def get_csv(params):
    if 'vw' not in params:
        params['vw'] = 0
    params['db'] = 'stocks'
    _parse_page_content(requests.get(URL, params=params).content)


def _parse_page_content(content):
    soup = BeautifulSoup(str(content), 'lxml')
    table = soup.find('table', attrs={'border': 1,
                                      'cellpadding': 2,
                                      'cellspacing': 0,
                                      'width': '100%'})
    with open('screener_data.csv', 'w') as f:
        writer = csv.writer(f)
        for row in table.find_all('tr'):
            temp = []
            for cell in row.find_all('td'):
                temp.append(unicode(cell.text).encode('utf-8'))
            writer.writerow(temp)
