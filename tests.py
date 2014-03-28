"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/26/2014
VERSION: 0.1.0

DONE:
== TESTS ==

TODO:
+ Finish tests once db.error() is its own error class derived from pythons error module
"""

import unittest
import sys

class SimplisticTest(unittest.TestCase):
    def setUp(self):
        import db
        self.t = db.DB(":memory:")

    def tearDown(self):
        self.t.closeDB()

    def test_createTable(self):
        from errors import DuplicateTableError, SyntaxError
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


##    def test_closeDB(self):
##        #Close an open DB => True
##        self.assertTrue(self.t.closeDB())
##        #Close an closed DB => False
##        self.assertFalse(self.t.closeDB())
##
##    #NOT FINISHED
##    def test_dropTable(self):
##        #Create a table => True
##        self.assertTrue(self.t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
##        #Drop a table => True
##        self.assertTrue(self.t.dropTable('test'))
##        
##    #MOST LIKELY WONT PASS RIGHT NOW
##    def test_clearTable(self):
##        #Create a table => True
##        self.assertTrue(self.t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
##        #Clear existing table => True
##        self.assertTrue(self.t.clearTable('test'))
##        #Clear non-existant table => False
##        self.assertFalse(self.t.clearTable('foobar'))
        

if __name__ == '__main__':
    unittest.main()
    
