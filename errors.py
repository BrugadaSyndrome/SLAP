"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/26/2014
VERSION: 0.1.0

DONE:

TODO:
    
"""

class DBError(Exception):
    pass

class DuplicateTableError(DBError):
    def __init__(self, dup_table, db_name):
        self.dup_table = dup_table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) already exists in DB ({1}).".format(self.dup_table, self.db_name))

class SyntaxError(DBError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr("With the query: {0}".format(self.value))
