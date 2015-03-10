import csv

from base_scraper import BaseScraper
from stocks import StockScraper


class OptionScraper(BaseScraper):
    CALL_INDEX = 0
    PUT_INDEX = 1
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
    BASE_URL = 'http://finance.yahoo.com/q/op'
    _expiration_dates = None

    def _get_expiration_dates(self, url):
        soup = self._get_soup(url)
        contract_list = soup.find('select', class_='Start-0')
        contract_soup = self._convert_to_soup(contract_list)
        contract_names = contract_soup.find_all('option')
        contracts = {}
        for contract in contract_names:
            formatted_date = contract.text
            contracts[formatted_date] = contract['value']
        return contracts

    def _parse_table(self, table):
        contracts = []
        soup = self._convert_to_soup(table.tbody)
        for row in soup.find_all('tr'):
            contract = {}
            cells = [x for x in row.contents if x != '\n']
            for i, cell in enumerate(cells):
                cell = self._convert_to_soup(cell)
                contract[self.CONTRACT_KEYS[i]] = cell.text[1:-1]
            contracts.append(contract)
        return contracts

    def _get_data_for_exp_date(self, url, query_param):
        soup = self._get_soup('{}&date={}'.format(url, query_param))
        table = soup.find_all('table', class_='quote-table')
        return {
            'calls': self._parse_table(table[self.CALL_INDEX]),
            'puts': self._parse_table(table[self.PUT_INDEX])
        }

    def _write_all_data_to_csv(self, writer):
        writer.writerow(['Underlying:', options.pop('underlying')])
        writer.writerow(self.CONTRACT_KEYS)
        options = self.get_data()
        for date in options:
            writer.writerow([date])
            contracts = options[date]
            for option_type in contracts:
                writer.writerow([option_type])
                for contract in contracts[option_type]:
                    writer.writerow(
                        [contract[key] for key in self.CONTRACT_KEYS]
                    )

    def get_data(self, ticker):
        url = self._get_url(ticker)
        exp_dates = self._get_expiration_dates(url)
        data = {}
        for date, query_param in exp_dates.iteritems():
            data[date] = self._get_data_for_exp_date(url, query_param)
        data['underlying'] = StockScraper().get_data(ticker).get(ticker)
        return data

    def export_to_csv(self, filename=None):
        if not filename:
            filename = '{}options.csv'.format(self.ticker)
        with open(filename, 'w+') as f:
            writer = csv.writer(f)
            self._write_all_data_to_csv(writer)
