"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 4/6/2014
VERSION: 0.1.0

DONE:
== TESTS ==
+ test_clearTable (3/27/2014)
+ test_closeDB (3/27/2104)
+ test_createTable (3/27/2014)
+ test_deleteRow(4/6/2014)
+ test_dropTable (4/1/2014)
+ test_insertRow (4/6/2014)

TODO:
+ Finish tests for all db methods
"""

import unittest
import sys

class DBTest(unittest.TestCase):

    def test_createTable(self):
        #Setup
        from errors import DuplicateTableError, SyntaxError
        import db
        t = db.DB(":memory:")
        
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Create a duplicate table without syntax errors => DuplicateTableError
        self.failUnlessRaises(DuplicateTableError, t.createTable, 'test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a duplicate table with syntax errors => DuplicateTableError
        self.failUnlessRaises(DuplicateTableError, t.createTable, 'test', '(name TEXT, color TEXT, age , ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a unique table with syntax errors => SyntaxError
        self.failUnlessRaises(SyntaxError, t.createTable, 'dummy', 'name TEXT, color TEXT, age INTEGER ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a table => True
        self.assertTrue(t.createTable('dummy', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_closeDB(self):
        #Setup
        from errors import DBClosedError
        import db
        t = db.DB(":memory:")

        #Close an open DB => True
        self.assertTrue(t.closeDB())
        #Close an closed DB => DBClosedError
        self.failUnlessRaises(DBClosedError, t.closeDB)

        #No clean up necessary
    def test_clearTable(self):
        #Setup
        from errors import TableDNE_Error, SyntaxError
        import db
        t = db.DB(":memory:")
        
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Clear existing table => True
        self.assertTrue(t.clearTable('test'))
        #Clear non-existant table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.clearTable, 'fooey')
        #Clear with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.clearTable, 'fo#o*e%y')

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_deleteRow(self):
        #Setup
        from errors import TableDNE_Error, SyntaxError
        import db
        t = db.DB(":memory:")

        #Delete a row that exists => True
        #Delete a row that does not exist => RowDNE_Error
        #Delete a row with syntax errors => SyntaxError
        #Delete a row in a non-existant table => TableDNE_Error
        
        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_dropTable(self):
        #Setup
        from errors import TableDNE_Error, SyntaxError
        import db
        t = db.DB(":memory:")
        
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Drop an existing table => True
        self.assertTrue(t.dropTable('test'))
        #Drop an non-existing table => True
        self.assertTrue(t.dropTable('fooey'))
        
        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_insertRow(self):
        #Setup
        from errors import AdapterMissingError, ConstraintError, TableDNE_Error, SyntaxError, UniqueError
        import db
        import datetime, time
        t = db.DB(":memory:")

        #Create a table => True
        self.assertTrue(t.createTable('MTG', '(name TEXT UNIQUE, color TEXT, count INTEGER CHECK(count > 0), time datetime, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Insert a full row in an existing table => True
        self.assertTrue(t.insertRow('MTG', {'name': 'Plain', 'color': 'WH', 'count': 10}))
        #Insert a partial row in an existing table => True
        self.assertTrue(t.insertRow('MTG', {'name': 'Mountain', 'count': 10}))
        #Insert a row in an non-existant table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.insertRow, 'fooey', {'name': 'Plain', 'color': 'WH', 'count': 10})
        #Insert a row with data that breaks a UNIQUE constraint => UniqueError
        self.failUnlessRaises(UniqueError, t.insertRow, 'MTG', {'name': 'Mountain', 'count': 30})
        #Insert a row with data that breaks a PRIMARY KEY constraint => UniqueError
        self.failUnlessRaises(UniqueError, t.insertRow, 'MTG', {'ID': 1, 'count': 30})
        #Insert a row with data that does not pass a CHECK constraint => ConstraintError
        self.failUnlessRaises(ConstraintError, t.insertRow, 'MTG', {'name': 'Swamp', 'color': 'BK', 'count': -100})
        #Insert a row with data that has an adapter associated with it => True
        self.assertTrue(t.insertRow('MTG', {'time': datetime.datetime.now(), 'Name': 'Orion'}))
        #Insert a row with data that does not have an adapter => AdapterMissingError
        self.failUnlessRaises(AdapterMissingError, t.insertRow, 'MTG', {'ID': 25, 'count': {'foo': 'bar'}})
        #Insert a row with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.insertRow, 'MTG', {'I*D': 25, 'cou#nt': 30})
        
        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())


if __name__ == '__main__':
    unittest.main()
    
