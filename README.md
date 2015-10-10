## Quick Start

    >>> from scrapers.options import OptionScraper
    >>> option_scraper = OptionScraper()
    >>> option_scraper.get_data('GOOG')
    {
        'underlying': '34.11',
        expiration_date1: {
            'puts': {
                ...
            },
            'calls': {
                ...
            }
        },
        expiration_date2: {
            ...
        },
        ...
    }

`expiration_date` is a string formatted the same as yahoo.

The `'puts'` and `'calls'` dictionaries will contain
`key/value` pairs for all the available data from yahoo,
which at the time is:
- `'strike'`
- `'name'`
- `'last'`
- `'bid'`
- `'ask'`
- `'change'`
- `'%change'`
- `'volume'`
- `'interest'`
- `'volatility'`

All values are python strings.

## Stock Data

Get data for a single stock:

    >>> from scrapers.stocks import StockScraper
    >>> stock_scraper = StockScraper()
    >>> stock_scraper.get_data('AAPL')
        {
            'name': 'AAPL',
            'current': '300.00',
            'close': '299.76',
            ...
        }

Or you can retrieve a list of stocks:

    >>> stock_scraper.get_data(['AAPL', 'XON', 'GPRO'])

## Bond Data

    >>> from scrapers.bonds import BondScraper
    >>> bond_scraper = BondScraper()
    >>> bond_scraper.get_data()

        {
            'treasury': {
                '3 month': {
                    'yield': '0.00',
                    ...
                },
                ...
            },
            ...
        }

## Mutual Fund Data

    >>> from scrapers.mutual_funds import MutualFundScraper
    >>> mf_scraper = MutualFundScraper()
    >>> mf_scraper.get_risk_data('GFFRX')

        {
            'GFFRX': {
                '10 years': {
                    'alpha': u'N/A',
                    ...
                },
                '3 years': {
                    'alpha': u'-1.39',
                    ...
                },
                ...
            }
        }

Also, you can directly get the expense ratio:

    >>> mf_scraper.get_expense_ratio(['GFFRX', 'MDCAX'])

        {
            'GFFRX': '1.76',
            'MDCAX': '1.40'
        }

## CSV Exports

    >>> stock_scraper.export_to_csv()

or

    >>> stock_scraper.export_to_csv(filename='somerandomfilename.csv')

Lots more functionality to come. Stay tuned!
