"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/27/2014
VERSION: 0.1.0

DONE:
== TESTS ==
+ test_clearTable (3/27/2014)
+ test_closeDB (3/27/2104)
+ test_createTable (3/27/2014)

TODO:
+ Finish tests for all db methods
"""

import unittest
import sys

class SimplisticTest(unittest.TestCase):

    def test_createTable(self):
        #Setup
        from errors import DuplicateTableError, SyntaxError
        import db
        self.t = db.DB(":memory:")
        
        #Create a table => True
        self.assertTrue(self.t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Create a duplicate table without syntax errors => DuplicateTableError
        self.failUnlessRaises(DuplicateTableError, self.t.createTable, 'test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a duplicate table with syntax errors => DuplicateTableError
        self.failUnlessRaises(DuplicateTableError, self.t.createTable, 'test', '(name TEXT, color TEXT, age , ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a unique table with syntax errors => SyntaxError
        self.failUnlessRaises(SyntaxError, self.t.createTable, 'dummy', 'name TEXT, color TEXT, age INTEGER ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
        #Create a table => True
        self.assertTrue(self.t.createTable('dummy', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))

        #Clean up
        #Close an open DB => True
        self.assertTrue(self.t.closeDB())

    def test_closeDB(self):
        #Setup
        from errors import DBClosedError
        import db
        self.t = db.DB(":memory:")

        #Close an open DB => True
        self.assertTrue(self.t.closeDB())
        #Close an closed DB => DBClosedError
        self.failUnlessRaises(DBClosedError, self.t.closeDB)

        #No clean up necessary5

    def test_clearTable(self):
        #Setup
        from errors import TableDNE_Error, SyntaxError
        import db
        self.t = db.DB(":memory:")
        
        #Create a table => True
        self.assertTrue(self.t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Clear existing table => True
        self.assertTrue(self.t.clearTable('test'))
        #Clear non-existant table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, self.t.clearTable, 'foobar')
        #Clear with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, self.t.clearTable, 'fo#o*e%y')

        #Clean up
        #Close an open DB => True
        self.assertTrue(self.t.closeDB())

##    #NOT FINISHED
##    def test_dropTable(self):
##        #Create a table => True
##        self.assertTrue(self.t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
##        #Drop a table => True
##        self.assertTrue(self.t.dropTable('test'))
##        

        

if __name__ == '__main__':
    unittest.main()
    
