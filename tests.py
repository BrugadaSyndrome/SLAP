"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/4/2014
VERSION: 0.0.1

== TESTS ==
+ test_clearTable (3/27/2014)
+ test_closeDB (3/27/2104)
+ test_createTable (3/27/2014)
+ test_deleteRow (4/21/2014)
+ test_dropTable (4/26/2014)
+ test_getColumnNames (4/22/2014)
+ test_getConstraints (5/3/2014)
+ test_getDBName (5/4/2014)
+ test_getRow (4/22/2014)
+ test_getValues (4/28/2014)
+ test_insertRow (4/6/2014)
+ test_parameterize (5/4/2014)
+ test_updateRow (5/3/2014)

TODO:
-[V 0.0.1]
    - test_parameterize needs to have its tests updated (see todo in method)
"""

import unittest

class DBTest(unittest.TestCase):

    def test_createTable(self):
        #Setup
        from errors import DuplicateTableError, SyntaxError
        import slap
        t = slap.DB()
        
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
        import slap
        t = slap.DB()

        #Close an open DB => True
        self.assertTrue(t.closeDB())
        #Close an closed DB => DBClosedError
        self.failUnlessRaises(DBClosedError, t.closeDB)

        #No clean up necessary
        
    def test_clearTable(self):
        #Setup
        from errors import SyntaxError, TableDNE_Error
        import slap
        t = slap.DB()
        
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
        from errors import ColumnDNE_Error, SyntaxError, TableDNE_Error
        import slap
        t = slap.DB()

        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Insert full rows in an existing table => True
        self.assertTrue(t.insertRow('test', {'name': 'Plain', 'color': 'WH', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Mountain', 'color': 'RD', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Swamp', 'color': 'BK', 'age': 10}))
        #Delete a row that exists => True
        self.assertTrue(t.deleteRow('test', {'ID': ('==', 1)}))
        #Delete a row that exists using multiple conditions => True
        self.assertTrue(t.deleteRow('test', {"ID": ('==', 2), 'name': ('==', 'Swamp')}))
        #Delete a row with a column that does not exist => ColumnDNE_Error
        self.failUnlessRaises(ColumnDNE_Error, t.deleteRow, 'test', {'junk': ('==', 'bar')})
        #Delete a row in a non-existant table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.deleteRow, 'fooey', {'name': ('==', 'Swamp')})
        #Delete a row with syntax errors => SyntaxError
        self.failUnlessRaises(SyntaxError, t.deleteRow, 'test', {'col(or': ('==', 'RD')})
        
        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_dropTable(self):
        #Setup
        from errors import SyntaxError
        import slap
        t = slap.DB()
        
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Drop an existing table => True
        self.assertTrue(t.dropTable('test'))
        #Drop an non-existing table => True
        self.assertTrue(t.dropTable('fooey'))
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Drop an existing table with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.dropTable, 't#st')
        
        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_getColumnNames(self):
        #Setup
        from errors import TableDNE_Error
        import slap
        t = slap.DB()
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))

        #Get column names from an existing table => (test, ['name', 'color', 'age', 'ID']
        self.assertEquals(t.getColumnNames('test'), ('test', ['name', 'color', 'age', 'ID']))
        #Get column names from an non-existing table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.getColumnNames, 'fooey')

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_getConstraints(self):
        #Setup
        from errors import TableDNE_Error
        import slap
        t = slap.DB()
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER CHECK(age > 0), ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Create a table => True
        self.assertTrue(t.createTable('test2', '(name TEXT, color TEXT, age INTEGER CHECK(age < 21), ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))

        #Get constraints on an existing table => [('test', ['ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'], ['age INTEGER CHECK(age > 0)'])]
        self.assertEquals(t.getConstraints('test'), [('test', ['ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'], ['age INTEGER CHECK(age > 0)'])])
        #Get constraints on an non-existing table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.getConstraints, 'foobar')

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_getDBName(self):
        #Setup
        import slap
        t = slap.DB(':memory:')

        #Get name of DB => 'someWeirdName'
        self.assertEquals(t.getDBName(), ':memory:')

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_getRow(self):
        #Setup
        from errors import ColumnDNE_Error, SyntaxError, TableDNE_Error
        import slap
        t = slap.DB()
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Insert full rows in an existing table => True
        self.assertTrue(t.insertRow('test', {'name': 'Plain', 'color': 'WH', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Mountain', 'color': 'RD', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Swamp', 'color': 'BK', 'age': 10}))

        #Get with one value
        self.assertEquals(t.getRow('test', {'ID': 1}), [(u'Plain', u'WH', 10, 1)])
        #Get with multiple values
        self.assertEquals(t.getRow('test', {'name': 'Mountain', 'color': 'RD', 'age': 10}), [(u'Mountain', u'RD', 10, 2)])
        #Get with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.getRow, 'test', {'n#ame': 'Mountain', 'col&or': 'RD', 'ag@e': 10})
        #Get with non-existing table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.getRow, 'fooey', {'name': 'Mountain', 'color': 'RD', 'age': 10})
        #Get with non-existing column => ColumnDNE_Error
        self.failUnlessRaises(ColumnDNE_Error, t.getRow, 'test', {'junk': 'bar'})

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_getValues(self):
        #Setup
        from errors import ColumnDNE_Error, SyntaxError, TableDNE_Error
        import slap
        t = slap.DB()
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Insert full rows in an existing table => True
        self.assertTrue(t.insertRow('test', {'name': 'Plain', 'color': 'WH', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Mountain', 'color': 'RD', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Swamp', 'color': 'BK', 'age': 10}))

        #Get values with one key => [(1, u'Plain')]
        self.assertEquals(t.getValues('test', 'ID, name', {'ID': 1}), [(1, u'Plain')])
        #Get values with multiple keys => []
        self.assertEquals(t.getValues('test', 'ID, name', {'ID': 1, 'color': ('!=', 'WH')}), [])
        #Get values with a non-existing column => ColumnDNE_Error
        self.failUnlessRaises(ColumnDNE_Error, t.getValues, 'test', 'ID, fooey', {'ID': 1})
        #Get values with a syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.getValues, 'test', 'I@D', {'ID': 'hello'})
        #Get values with a non-existing table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.getValues, 'fooey', 'ID', {'ID': 'hello'})

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_insertRow(self):
        #Setup
        from errors import AdapterMissingError, ConstraintError, TableDNE_Error, SyntaxError, UniqueError
        import slap
        import datetime
        t = slap.DB()

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

    def test_parameterize(self):
        #TODO: Need to test the second item returned by test_paramterize

        #Setup
        import slap
        import parameterize as param
        t = slap.DB()

        #Seperate values with param dict  => "('Count, Name, Number', ':Count, :Name, :Number')"
        self.assertEquals(param.paramTuple({'Name': 'Test', "Number": 9, "Count": 20}), ('Count, Name, Number', ':Count, :Name, :Number'))
        #Seperate values with param dict  => "('Count, Name, Number', ':Count, :Name, :Number')"
        self.assertEquals(param.paramTupleDebug({'Name': 'Test', "Number": 9, "Count": 20}), ('Count, Name, Number', '20, Test, 9'))
        #Join keys with key lookups and equal comparisons  => "Count=:Count, Name=:Name, Number=:Number"
        self.assertEquals(param.paramComma({'Name': 'Test', "Number": 9, "Count": 20}), "Count=:Count, Name=:Name, Number=:Number")
        #Join keys with key and different comparators => "Count<:Count AND NOT Name=:Name AND Number=:Number"
        self.assertEquals(param.paramKey({'Name': ('!=', 'Test'), "Number": 9, "Count": ("<", 20)})[0], "Count<:Count AND NOT Name=:Name AND Number=:Number")
        #Join keys with key values and different comparators => 'Count<20 AND NOT Name="Test" AND Number=9'
        self.assertEquals(param.paramDebug({'Name': ('!=', 'Test'), "Number": ("==", 9), "Count": ("<", 20)}), 'Count<20 AND NOT Name="Test" AND Number=9')

        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

    def test_updateRow(self):
        #Setup
        from errors import ColumnDNE_Error, SyntaxError, TableDNE_Error
        import slap
        t = slap.DB()
        #Create a table => True
        self.assertTrue(t.createTable('test', '(name TEXT, color TEXT, age INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)'))
        #Insert full rows in an existing table => True
        self.assertTrue(t.insertRow('test', {'name': 'Plain', 'color': 'WH', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Mountain', 'color': 'RD', 'age': 10}))
        self.assertTrue(t.insertRow('test', {'name': 'Swamp', 'color': 'BK', 'age': 10}))

        #Update one column => True
        self.assertTrue(t.updateRow('test', {'name': 'Forest'}, {'ID': 1}))
        #Update one column with multiple constraints => True
        self.assertTrue(t.updateRow('test', {'name': 'Plain'}, {'ID': 1, 'age': 10}))
        #Update multiple columns => True
        self.assertTrue(t.updateRow('test', {'name': 'Island', 'color': 'BL'}, {'ID': 1}))
        #Update multiple columns with multiple constraints => True
        self.assertTrue(t.updateRow('test', {'name': 'Island', 'color': 'BL'}, {'ID': 1, 'age': ('<=', 10)}))
        #Update with non-existing table => TableDNE_Error
        self.failUnlessRaises(TableDNE_Error, t.updateRow, 'tut', {'name': 'Island', 'color': 'BL'}, {'ID': 1, 'age': ('<=', 10)})
        #Update with non-existing column => ColumnDNE_Error
        self.failUnlessRaises(ColumnDNE_Error, t.updateRow, 'test', {'nam*e': 'Island', 'color': 'BL'}, {'ID': 1, 'age': ('<=', 10)})
        #Update with syntax error => SyntaxError
        self.failUnlessRaises(SyntaxError, t.updateRow,'test', {'nam#e': 'Island', 'color': 'BL'}, {'ID': 1, 'age': ('<=', 10)})


        #Clean up
        #Close an open DB => True
        self.assertTrue(t.closeDB())

if __name__ == '__main__':
    unittest.main()
