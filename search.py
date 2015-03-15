from pprint import pprint

import requests
from bs4 import BeautifulSoup


URL = 'http://screener.finance.yahoo.com/stocks.html'


def format_titles(titles):
    titles = titles = [title.text.replace(':', '') for title in titles]
    formatted_titles = []
    for i, title in enumerate(titles):
        if title == 'Min':
            formatted_titles.pop()
            formatted_titles.append(
                '{} Min'.format(titles[i-1])
            )
        elif title == 'Max':
            formatted_titles.append(
                '{} Max'.format(titles[i-2])
            )
        else:
            formatted_titles.append(title)
    return formatted_titles


soup = BeautifulSoup(requests.get(URL).content, 'lxml')

selects = soup.find_all('select')
titles = soup.find_all('font', attrs={'face': 'arial', 'size':'-1'})
titles.pop(0)
titles = format_titles(titles)

choices = { select['name']: title for select, title in zip(selects, titles)}

pprint(choices)
