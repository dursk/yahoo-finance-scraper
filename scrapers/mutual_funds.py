from base_scraper import BaseScraper


class MutualFundScraper(BaseScraper):

    BASE_URL = 'http://finance.yahoo.com/q/rk'

    KEYS = [
        'alpha',
        'beta',
        'mean_annual_return',
        'r-squared',
        'std_dev',
        'sharpe_ratio',
        'treynor_ratio',
    ]

    DATA_LENGTHS = [
        '3 years',
        '5 years',
        '10 years',
    ]

    def _parse_table(self, soup):
        data = {}
        cells = soup.find_all('td', class_='yfnc_tabledata1')
        for i, cell in enumerate(cells[::3]):
            curr_index = i * 3
            data[self.KEYS[i]] = cells[curr_index + 1].text
        return data

    def _parse_tables(self, soup):
        data = {}
        tables = soup.find_all(class_='yfnc_tableout1')
        for length, table in zip(self.DATA_LENGTHS, tables):
            table = self._convert_to_soup(table)
            data[length] = self._parse_table(table)
        return data

    def get_data(self, tickers):
        if type(tickers) is str:
            tickers = [tickers]
        data = {}
        for ticker in tickers:
            url = self._get_url(ticker)
            soup = self._get_soup(url)
            data[ticker] = self._parse_tables(soup)
        return data
