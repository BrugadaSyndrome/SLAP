"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/27/2014
VERSION: 0.1.0

DONE:
== Errors ==
+ DBClosedError (3/27/2014)
+ DuplicateTableError (3/27/2014)
+ SyntaxError (3/27/2014)
+ TableDNE_Error (3/27/2014)

TODO:
    
"""
import sqlite3 as sql

class DBError(Exception):
    pass

class DBClosedError(DBError):
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return repr("The DB ({0}) is already closed.".format(self.table))

class DuplicateTableError(DBError):
    def __init__(self, dup_table, db_name):
        self.dup_table = dup_table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) already exists in DB ({1}).".format(self.dup_table, self.db_name))

class SyntaxError(DBError):
    def __init__(self, query):
        self.query = query

    def __str__(self):
        return repr("With the query: {0}".format(self.query))

class TableDNE_Error(DBError):
    def __init__(self, dup_table, db_name):
        self.dup_table = dup_table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) does not exists in DB ({1}).".format(self.dup_table, self.db_name))
