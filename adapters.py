"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/3/2014
VERSION: 0.0.1

DONE:
== Adaptors ==
+   adapt_datetime(datetime.datetime.now()) => float (3/23/2014)
+ extract_datetime(float) => datetime.datetime.now() (3/23/2014)

TODO:
- [V 0.0.2]
    - Person/Name Class(first, middle, last)

- [V 0.0.3]
    - !! Encrypt all personal data put into db !!

"""

import sqlite3 as sql
import datetime, time

#Creator adaptor functions
def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

def extract_datetime(f):
    return datetime.datetime.fromtimestamp(time.mktime(time.localtime(f)))

#Register Adapters
sql.register_adapter(datetime.datetime, adapt_datetime) 
