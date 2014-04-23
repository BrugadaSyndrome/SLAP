"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 4/6/2014
VERSION: 0.1.0

DONE:
== Errors ==
+ AdapterMissingError (4/6/2014)
+ DBClosedError (3/27/2014)
+ ColumnDNE_Error (4/6/2014)
+ ConstraintError (4/6/2014)
+ DuplicateTableError (3/27/2014)
+ SyntaxError (3/27/2014)
+ TableDNE_Error (4/6/2014)
+ UniqueError (4/6/2014)

TODO:
    
"""

class DBError(Exception):
    pass

class AdapterMissingError(DBError):
    def __init__(self, obj_type, table, db_name):
        self.obj_type = obj_type
        self.table = table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) in DB ({1}) has no adapter for the object of ({2})".format(self.table, self.db_name, type(self.obj_type)))

class ColumnDNE_Error(DBError):
    def __init__(self, dne_column, table, db_name):
        self.dne_column = dne_column
        self.table = table
        self.db_name = db_name

    def __str__(self):
        return repr("Column ({0}) does not exist in table ({1}) in DB ({2}).".format(self.table, self.dne_column, self.db_name))

class ConstraintError(DBError):
    def __init__(self, query, constraints, table, db_name):
        self.query = query
        self.constraints = constraints
        self.table = table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) in DB ({1}) has constraints:\n {2}\n that are being violated with the query:\n {3}". format(self.table, self.db_name, self.constraints, self.query))

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
    def __init__(self, dne_table, db_name):
        self.dne_table = dne_table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) does not exists in DB ({1}).".format(self.dne_table, self.db_name))

class UniqueError(DBError):
    def __init__(self, query, constraints, table, db_name):
        self.query = query
        self.constraints = constraints
        self.table = table
        self.db_name = db_name

    def __str__(self):
        return repr("Table ({0}) in DB ({1}) has unique fields:\n {2}\n that are being violated with the query:\n {3}". format(self.table, self.db_name, self.constraints, self.query))
