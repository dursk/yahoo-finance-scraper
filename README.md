## Quick Start

    import options_scraper

    options_scraper.get_options_data('XON')

You will get back a dictionary of the following form:

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

where `expiration_date` is a python `datetime` object.

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
