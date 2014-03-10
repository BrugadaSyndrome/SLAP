"""
AUTHOR: COBY JOHNSON
PROJECT: SQLite3-DB
LAST UPDATE: 3/10/2014
VERSION: 0.2.0

DONE:
== Constructors / Destructors==
+ DB.init

== Modify Table (Setters) ==
+ DB.createTable
+ DB.dropTable
+ DB.closeDB

== Getters ==
+ DB.getColumnNames
+ DB.getConstraints

== Utilities ==
+ DB.dictToStrings
+ DB.printTable

== Error Reporting ==
+ DB.error
+ DB.warning


TODO:
-!!!NEED TO MAKE ALL FUNCTIONS SAFE FROM SQL INJECTION ATTACKS!!!-

-REVISIT ALL FUNCTIONS NOT IN DONE LIST AND FIX TO USE DICTIONARY PARAMETERS

-PROPERLY TEST INNER JOIN FUNCTION TO PROVE FUNCTIONALITY
    -WRITE COMMENTS ON PARAMETERS

+DONE: MADE INSERT ROW UPDATE COUNT WITH UNIQUE TEXT CONSTRAINT+
-FINSH UPDATING INSERT ROW TO HANDLE UNIQUE CONSTRAINTS THAT ARE NUMBERS
    -MAKE THIS WORK WITH MULTIPLE UNIQUE CONSTRAINTS

-MODIFY ALTER TABLE FUNCTION TO BE ABLE TO DROP TABLE AND RENAME COLUMNS BY:
    -HAVING IT COPY INFO TO NEW TABLE AND THEN RENAMING THE TABLE WHEN DROPPING A COLUMN
    -HAVING IT COPY INFO TO NEW TABLE BUT RENAME THE COLUMN THAT NEEDS TO BE RENAMED

-LOOK INTO ADAPTERS LINKING A DATATYPE TO STRING CONVERSION FUNCTION FOR STORAGE IN SQL DB

----------------------------------------
EVENTUALLY DO SOMETIME IN THE FAR FUTURE:
-STOP HACKERS BY SCARING THE CRAP OUT OF THEM IF THEY TRY INTENTIALLY MALICOUS CODE
    -RETURN URL PAGE WITH THEIR HOME ADDRESS AND SAYING WE HAVE NOTIFED THE LOCAL FBI
     OF THEIR ILLEGAL ACTIVITIES.
"""

import sqlite3 as sql

class DB:
    def __init__(self, name):
        #Load DB
        self.db = sql.connect(name)
        #Create DB cursor
        self.cursor = self.db.cursor()

    #createTable(self,
    #            table, #Table name
    #            info)  #(Column_name_1, ..., Column_name_X)
    def createTable(self, table, info):
        try:
            #print '''CREATE TABLE {0} {1}'''.format(table, info)
            self.cursor.execute('''CREATE TABLE {0} {1}'''.format(table, info))
            self.db.commit()
            return
        except:
            self.error('Table "{0}" already exists.'.format(table))
        
    #dropTable(self,
    #          table) #Table name
    def dropTable(self, table, force=False):
        answer = 'n'
        if (force == False):
            self.warning('This will delete table "{0}" with all of it data'.format(table))
            answer = raw_input('Are you sure you want to drop table "{0}"? (y/N)'.format(table))
        if (answer.lower == 'y' or force == True):
            #print '''DROP TABLE IF EXISTS {0}'''.format(table)
            self.cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(table))
            self.db.commit()
        else:
            print 'Disaster averted. Table "{0}" was not changed.'.format(table)
        return

    #clearTable(self,
    #           table) #Table name
    def clearTable(self, table, force=False):
        answer = 'n'
        if (force == False):
            self.warning('This will delete all data from table "{0}"'.format(table))
            answer = raw_input('Are you sure you want to delete all records from table "{0}"? (y/N)'.format(table))
        if (answer.lower() == 'y' or force == True):
            self.cursor.execute('''DELETE FROM {0}'''.format(table))
            self.db.commit()
            print 'Table "{0}" successfully cleared.'.format(table)
        else:
            print 'Disaster averted. Table "{0}" was not changed.'.format(table)

##    #alterTable(self,
##    #           table,   #Table
##    #           command) #SUPPORTS ADD column, RENAME TO table
##    ### NOTE: SQLITE3 DOES NOT SUPPORT: RENAME column, DROP column ###
##    def alterTable(self, table, command):
##        #print 'ALTER TABLE {0} {1}'.format(table, command)
##        self.cursor.execute('''ALTER TABLE {0} {1}'''.format(table, command))
##        self.db.commit()
##        return

    #insertRow(self,
    #          row,  #ROW NAME
    #          info) #{key0:value0, ..., keyX:valueX}
    def insertRow(self, row, info):
        (keys, values) = self.paramDict(info)
        print '''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values)
        try:
            #Will add row to DB unless there is a duplicate PRIMARY/UNIQUE key constraint.
            self.cursor.execute('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values), info)
            self.db.commit()
            return
        except sql.IntegrityError:
            #Tell user to inherit and overwrite this method
            print info
            raise NotImplementedError('Could not insert row: You need to implement how you want to merge your ADT.')
        
##    #deleteRow(self,
##    #          row,       #ROW NAME
##    #          condition) #INSERT CONDITIONAL STATEMENT   
##    def deleteRow(self, row, condition):
##        #print '''DELETE FROM {0} WHERE {1}'''.format(row, condition)
##        self.cursor.execute('''DELETE FROM {0} WHERE {1}'''.format(row, condition))
##        self.db.commit()
##        return

##    #getRowByID(self,
##    #           row,  #ROW NAME
##    #           ID)   #ID OF ROW TO RETURN
##    def getRowByID(self, row, ID):
##        #print '''SELECT * FROM {0} WHERE ID={1}'''.format(row, ID)
##        self.cursor.execute('''SELECT * FROM {0} WHERE ID=?'''.format(row), (ID))
##        result = self.cursor.fetchone()
##        if (result == None):
##            print '##### No data from table "{0}" exists with ID "{1}" #####'.format(row, ID)
##        return result

##    #getRow(self,
##    #           row,       #ROW NAME
##    #           condition) #ID OF ROW TO RETURN
##    def getRow(self, row, condition):
##        print '''SELECT * FROM {0} WHERE {1}'''.format(row, condition)
##        self.cursor.execute('''SELECT * FROM {0} WHERE {1}'''.format(row, condition))
##        result = self.cursor.fetchone()
##        if (result == None):
##            print '##### No data from table "{0}" exists with statement "{1}" #####'.format(row, condition)
##        return result

##    #updateRow(self,
##    #          row,    #ROW NAME
##    #          column, #COLUMN NAME
##    #          value,  #NEW COLUMN VALUE
##    #          ID)     #ID OF ROW
##    def updateRow(self, row, column, value, ID):
##        print '''UPDATE {0} SET {1}={2} WHERE ID={3}'''.format(row, column, value, ID)
##        self.cursor.execute('''UPDATE {0} SET {1}=? WHERE ID=?'''.format(row, column), (value, ID))
##        self.db.commit()
##        return

##    #innerJoin(self,
##    #          table1,    #
##    #          column1,   #
##    #          table2,    #
##    #          column2,   #
##    #          condition) #
##    def innerJoin(self, table1, column1, table2, column2, condition):
##        print '''SELECT {0}.{1}, {2}.{3} FROM {0} JOIN {2} ON {4}'''.format(table1, column1, table2, column2, condition)
##        self.cursor.execute('''SELECT {0}.{1}, {2}.{3} FROM {0} JOIN {2} ON {4}'''.format(table1, column1, table2, column2, condition))
##        results = self.cursor.fetchall()
##        return results

    #printTable(self,
    #           table) #Table name
    def printTable(self, table):
        cursor = self.cursor.execute('''SELECT * FROM {0}'''.format(table))
        for row in cursor:
            print row
        return

    #getColumnNames(self,
    #               table) #Table name
    """
    Returns all the columns name values
    Returns in the format (tableName, [columnNames])
    """
    def getColumnNames(self, table):
        #Get table header from DB
        d = {}
        d['name'] = table
        self.cursor.execute("select * from sqlite_master where name=(:name)", d)
        schema = self.cursor.fetchone()
        #Does the table exist?
        if (schema == None):
            self.error('Failed to find column names: Table does not exist.')
        #Find the paranthesis
        lp = schema[4].find('(') + 1
        rp = schema[4].rfind(')')
        #Type cast from unicode to string
        schema = str(schema[4])
        #Splice out the columnnames
        schema = schema[lp:rp]
        temp = schema.split(',')
        #Remove white space
        columns = []
        for item in temp:
            columns.append(item.strip())
        #pull names out and discard restraints
        names = []
        for n in columns:
            sp = n.find(' ')
            temp = n[:sp]
            names.append(temp)
        return (table, names)

    #paramDict(self,
    #          info)    #Dictionary to parse
    """
    Parameterizes a dictionary into appropriate string values
    """
    def paramDict(self, info):
        keys = ""
        values = ""
        for k in info.keys():
            keys += k + ", "
            values += ":" + k + ", "
        keys = keys[:len(keys)-2]
        values = values[:len(values)-2]
        #strings look like this
        #   "key0, ..., keyX"
        #   ":value0, ..., :valueX"
        return (keys, values)

    #getConstraints(self,
    #               table) #Table name
    """
    Returns all the table columns that are under a unique/primary key restraint
    Returns in the format [(table_name, [column info]), ..., (table_name, [column info])]
    """
    def getConstraints(self, table="ALL"):
        
        #Find all constraints in all tables
        if (table == "ALL"):
            #Get all table headers from DB
            self.cursor.execute("select * from sqlite_master")
            schema = self.cursor.fetchall()
            #Pull out user created tables
            T = []
            for item in schema:
                if (item[0] == 'table' and item[1] != 'sqlite_sequence'):
                    T.append(item)
            #Pull out unique constraints for each table
            U = []
            for item in T:
                U.append(self.getConstraints(item[1])[0])
            return U

        #Find constraints in a specific table
        else:
            #Get table header from DB
            d = {}
            d['name'] = table
            self.cursor.execute("select * from sqlite_master where name=(:name)", d)
            schema = self.cursor.fetchone()
            #Does the table exist?
            if (schema == None):
                self.error('Failed to find constraints: Table does not exist.')
            #Find the paranthesis
            lp = schema[4].find('(') + 1
            rp = schema[4].rfind(')')
            #Type cast from unicode to string
            schema = str(schema[4])
            #Find table name before next step
            name = schema[:lp-1]
            temp = name.lower()
            n = temp.find('create table')
            name = name[n+12:].strip()
            #Splice out the columnnames
            schema = schema[lp:rp]
            temp = schema.split(',')
            #Remove white space
            columns = []
            for item in temp:
                columns.append((item.strip(), item.lower().strip()))
            #Pull out unique/primary key constraints and return
            unique = []
            for item in columns:
                if (item[1].find('unique') != -1 or item[1].find('primary key') != -1):
                    unique.append(item[0])
            return [(name, unique)]

    #closeDB(self)
    def closeDB(self):
        #Save database
        self.db.commit()
        #Close cursor
        self.cursor.close()
        #Close database
        self.db.close()
        return

    #error(self,
    #      message) #Error message to be displayed
    def error(self, message):
        self.db.rollback()
        self.closeDB()
        raise Exception('### {0} ###'.format(message))

    #warning(self,
    #        message) #Warning message to be displayed
    def warning(self, message):
        print '=== {0}! ==='.format(message)
        return

    #safe(self) #Prevents SQL Injection attacks
    def safe(self, string):
        safe_chars = 'abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMONPQRSTUVWXYZ0123456789@.-_+'
        for c in string:
            if not(c in safe_chars):
                return 'False: {0}'.format(string)
        return 'True: {0}'.format(string)

def main():
    db = DB('MTG.sql')

##    hack = "ilovehackers@hackers.net"
##    print db.safe(hack)
##    hack = "anything' or 'x'='x'"
##    print db.safe(hack)
##    hack = "steve@unixwiz.net'"
##    print db.safe(hack)
##    hack = "x' AND email IS NULL; --"
##    print db.safe(hack)
##    hack = "x' AND 1=(SELECT COUNT(*) FROM tabname); --"
##    print db.safe(hack)
##    hack = "x' AND members.email IS NULL; --"
##    print db.safe(hack)

    db.dropTable('MTG', 1)
    db.dropTable('Test', 1)

    db.createTable('MTG', '(name TEXT UNIQUE, color TEXT, count INTEGER CHECK(count > 0), ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
    db.insertRow('MTG', {'name': 'Plain', 'color': 'WH', 'count': 50})
    db.insertRow('MTG', {'name': 'Swamp', 'color': 'BK', 'count': 50})
    db.insertRow('MTG', {'name': 'Swamp', 'color': 'BK', 'count': 50})

    #db.createTable('Test', '(test TEXT, name INTEGER PRIMARY KEY)')

    #GET THIS TO WORK WITH MULTIPLE TABLES IN DATABASE

    #print db.getConstraints('MTG')
    #print db.getConstraints('Test')
    #print db.getConstraints()

    #print db.clearTable('MTG')
    #print db.getColumnNames('MTG')

    #db.printTable('MTG')
    
    db.closeDB()

main()
