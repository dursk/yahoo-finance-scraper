from itertools import izip
from pprint import pprint

import requests
from bs4 import BeautifulSoup


URL = 'http://screener.finance.yahoo.com/stocks.html'


def format_field_names(titles):
    titles = [title.text.replace(':', '') for title in titles]
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

field_ids = soup.find_all('select')
field_names = soup.find_all('font', attrs={'face': 'arial', 'size':'-1'})
field_names.pop(0)
field_names = format_field_names(field_names)

choices = {
    field_id['name']: field_name
    for field_id, field_name in izip(field_ids, field_names)
}

choices_with_options = {}

for field in field_ids:
    temp = {}
    for option in field.children:
        if not option.text.strip().startswith('---'):
            temp[option['value']] = str(option.text.strip().replace('\n', ' '))
    choices_with_options[field['name']] = temp

pprint(choices_with_options)
