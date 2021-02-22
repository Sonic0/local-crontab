<p align="center">
  <img src="https://raw.githubusercontent.com/Sonic0/local-crontab/main/logo.png" title="Cron-converter">
</p>

local-crontab is a Python wheel and command line utility to convert a crontab, in a local timezone, into a set of UTC crontabs. 
It creates multiple UTC crontabs because of Daylight Saving Time.<br>
This project is based to [local-crontab](https://github.com/UnitedIncome/local-crontab) by [UnitedIncome](https://github.com/UnitedIncome) with some bugfixs.

## Use it online!
TODO

## Use as a script
```
$ local-crontab --help
Usage: command_line.py [OPTIONS] CRONTAB

  Convert a crontab, in a localized timezone, into a set of UTC crontabs.

Options:
  --t, --timezone TZ    The timezone to use. Defaults to system timezone
  --help                Show this help message and exit.
  --version             Show program's version number and exit.

# year 2021
$ local-crontab --timezone America/New_York '0 10 * * *'
0 15 * 1-2 *
0 15 1-13 3 *
0 14 14-31 3 *
0 14 * 4-10 *
0 14 1-6 11 *
0 15 7-30 11 *
0 15 * 12 *

# year 2021
$ local-crontab --timezone America/Denver '0 10 * * *'
0 17 * 1-2 *
0 17 1-13 3 *
0 16 14-31 3 *
0 16 * 4-10 *
0 16 1-6 11 *
0 17 7-30 11 *
0 17 * 12 *
```

## Use as a library
Install with `pip install local-crontab`, then:
```python
from local_crontab import Converter
Converter('0 10 * * *', 'America/New_York').to_utc_crons()
# returns
[ '0 15 * 1-2,12 *',                                               
  '0 15 1-10 3 *',                                                 
  '0 14 11-31 3 *',                                                
  '0 14 * 4-10 *',                                                 
  '0 14 1-3 11 *',                                                 
  '0 15 4-31 11 *' ]                                               
```
