## Quick Start

Run `main.py` at the command line and pass it whichever ticker symbol you so please.
You will get back a dictionary of the following form:

    {
        expiration_date: {
            'puts': {
                ...
            },
            'calls': {
                ...
            }
        }
    }

where `expiration_date` is a python `datetime` object.

`'puts'` and `'calls'` will contain `key/value` pairs for all
the available data from yahoo.
