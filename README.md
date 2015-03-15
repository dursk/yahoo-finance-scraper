## Quick Start

    >>> from scraper.options import OptionScraper
    >>> scraper = OptionScraper()
    >>> scraper.get_data('GOOG')
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

All values are python strings.

## Stock Data

Get data for a single stock:

    >>> from scraper.stocks import StockScraper
    >>> scraper = StockScraper()
    >>> scraper.get_data('AAPL')
        {
            'name': 'AAPL',
            'current': '300.00',
            'close': '299.76',
            ...
        }

Or you can retrieve a list of stocks:

    >>> scraper.get_data(['AAPL', 'XON', 'GPRO'])

## Bond Data

    >>> from scraper.bonds import BondScraper
    >>> scraper = BondScraper()
    >>> scraper.get_data()

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

## CSV Exports

    >>> scraper.export_to_csv()

or

    >>> scraper.export_to_csv(filename='somerandomfilename.csv')

Lots more functionality to come. Stay tuned!
