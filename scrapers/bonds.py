from base_scraper import BaseScraper

from bs4 import BeautifulSoup


class BondScraper(BaseScraper):

    BASE_URL = 'http://finance.yahoo.com/bonds/composite_bond_rates'
    BOND_TYPES = [
        'treasury',
        'municipal',
        'corporate'
    ]
    BOND_KEYS = [
        'yield',
        'yesterday',
        'last week',
        'last month'
    ]

    def _parse_table(self, table):
        bonds = {}
        soup = self._convert_to_soup(table)
        rows = soup.find_all('tr')
        for row in rows[1:]:
            cells = [x for x in row.contents if x != '\n']
            maturity = cells[0].text
            bonds[maturity] = {}
            for i, cell in enumerate(cells[1:]):
                bonds[maturity][self.BOND_KEYS[i]] = cell.text
        return bonds


    def get_data(self):
        soup = self._get_soup(BASE_URL)
        bond_tables = soup.find_all('table', class_='yfirttbl')
        bonds = {}
        for i, table in enumerate(bond_tables):
            ret = self._parse_table(table)
            bonds[self.BOND_TYPES[i]] = ret
        return bonds
