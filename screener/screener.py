from itertools import izip

import requests
from bs4 import BeautifulSoup


URL = 'http://screener.finance.yahoo.com/stocks.html'


class StockScreener(object):

    def __init__(self):
        self._soup = None
        self._field_names = None
        self.field_options = None

    @property
    def soup(self):
        if self._soup:
            return self._soup
        self._soup = BeautifulSoup(requests.get(URL).content, 'lxml')
        return self._soup

    def _format_field_names(self, field_names):
        field_names = [title.text.replace(':', '') for title in field_names]
        formatted_field_names = []
        for i, title in enumerate(field_names):
            if title == 'Min':
                formatted_field_names.pop()
                formatted_field_names.append(
                    '{} Min'.format(field_names[i-1])
                )
            elif title == 'Max':
                formatted_field_names.append(
                    '{} Max'.format(field_names[i-2])
                )
            else:
                formatted_field_names.append(title)
        return [str(x) for x in formatted_field_names]

    def view_fields(self):
        if self._field_names:
            return self._field_names
        fields = self.soup.find_all('select')
        field_names = self.soup.find_all(
            'font', attrs={'face': 'arial', 'size': '-1'}
        )
        field_names.pop(0) # stupid header
        field_names = self._format_field_names(field_names)
        self._field_names = {
            field['name']: field_name
            for field, field_name in izip(fields, field_names)
        }
        return self._field_names

    # def view_field_options(self, field=None):
    #     if self._field_options:
    #         if not field:
    #             return self._field_options
    #         return self._field_options[field]

    #     if not self._field_names:
    #         self.view_fields()
