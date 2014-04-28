"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/23/2014
VERSION: 0.1.0

DONE:
== Adaptors ==
+   adapt_datetime(datetime.datetime.now()) => float (3/23/2014)
+ extract_datetime(float) => datetime.datetime.now() (3/23/2014)

TODO:
- [V 0.1.1]
    - Person/Name Class(first, middle, last)

- [V 0.2.0]
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
