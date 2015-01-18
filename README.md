## Quick Start

    >>> from scraper import OptionsScraper
    >>> scraper = OptionsScraper('GOOG')
    >>> scraper.get_data()
    {
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

    >>> from scraper import StockScraper
    >>> scraper = StockScraper('AAPL')
    >>> scraper.get_data()
        {
            'name': 'AAPL',
            'current': '300.00',
            'close': '299.76',
            ...
        }

## CSV Exports

    >>> scraper.export_to_csv()

or

    >>> scraper.export_to_csv(filename='somerandomfilename.csv')

Lots more functionality to come. Stay tuned!
