import csv

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
        soup = self._get_soup(self.BASE_URL)
        bond_tables = soup.find_all('table', class_='yfirttbl')
        bonds = {}
        for i, table in enumerate(bond_tables):
            ret = self._parse_table(table)
            bonds[self.BOND_TYPES[i]] = ret
        return bonds

    def export_to_csv(self, filename='bonds.csv'):
        with open(filename, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['maturity'] + self.BOND_KEYS)
            bonds = self.get_data()
            for bond_type in bonds:
                writer.writerow([bond_type])
                for maturity in bonds[bond_type]:
                    bond = bonds[bond_type][maturity]
                    prices = [bond[key] for key in self.BOND_KEYS]
                    writer.writerow([maturity] + prices)
