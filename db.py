"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/4/2014
VERSION: 0.2.3

DONE:
== Constructors / Destructors ==
+ DB.init (5/4/2014)

== Modify Table (Setters) ==
+ DB.createTable (3/27/2014)
+ DB.clearTable (4/1/2014)
+ DB.closeDB (3/27/2014)
+ DB.deleteRow (4/21/2014)
+ DB.dropTable (4/26/2014)
+ DB.insertRow (5/4/2014)
+ DB.updateRow (5/4/2014)

== Getters ==
+ DB.getColumnNames (4/22/2014)
+ DB.getConstraints (5/3/2014)
+ DB.getDBName (4/21/2014)
+ DB.getRow (5/4/2014)
+ DB.getTableNames (3/26/2014)
+ DB.getValues (5/4/2014)

TODO:
- [V 0.2.4] - Logging Mode
    - make a logging mode and a debugging mode module
        + logging mode will print each statement out to a file as they are executed
        + debugging mode will print each statement out to the console as they are executed

- [V 0.2.5] - Alter Table
    - Make an alterTable method
        + Extend the functionality to allow renaming tables and dropping tables

-!!!NEED TO MAKE ALL FUNCTIONS SAFE FROM SQL INJECTION ATTACKS!!!-

"""

from errors import *
import parameterize as param
import sqlite3 as sql

class DB:
    #__int__(self,
    #        name) #Name of the DB to be created
    def __init__(self, name=":memory:"):
        #Data members
        i = name.rfind('.')
        if (i != -1):
            self.name = name[:i]
        else:
            self.name = name

        #Load DB
        self.db = sql.connect(name)
        #Create DB cursor
        self.cursor = self.db.cursor()

    #createTable(self,
    #            table, #Table name
    #            info)  #(Column_name_1, ..., Column_name_X)
    def createTable(self, table, info):
        #print '''CREATE TABLE {0} {1}'''.format(table, info)
        try:
            self.cursor.execute('''CREATE TABLE {0} {1}'''.format(table, info))
            self.db.commit()
            return True
        except sql.OperationalError:
            if (table in self.getTableNames()):
                raise DuplicateTableError(table, self.getDBName())
            else:
                raise SyntaxError('''CREATE TABLE {0} {1}'''.format(table, info))
        
    #dropTable(self,
    #          table) #Table name
    def dropTable(self, table):
        #print '''DROP TABLE IF EXISTS {0}'''.format(table)
        try:
            self.cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(table))
            self.db.commit()
            return True
        except sql.OperationalError as e:
            if ("syntax error" in str(e)):
                raise SyntaxError('''DROP TABLE IF EXISTS {0}'''.format(table))

    #clearTable(self,
    #           table) #Table name
    def clearTable(self, table):
        #print '''DELETE FROM {0}'''.format(table)
        try:
            self.cursor.execute('''DELETE FROM {0}'''.format(table))
            self.db.commit()
            #print 'Table ({0}) successfully cleared.'.format(table)
            return True
        except sql.OperationalError as e:
            if ("syntax error" in str(e)):
                raise SyntaxError('''DELETE FROM {0}'''.format(table))
            elif not (table in self.getTableNames()):
                raise TableDNE_Error(table, self.getDBName())

    #insertRow(self,
    #          row,  #Row name
    #          info) #{key0:value0, ..., keyX:valueX}
    def insertRow(self, row, info):
        (keys, values) = param.paramTuple(info)
        #print '''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values)
        try:
            self.cursor.execute('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values), info)
            self.db.commit()
            return True
        #Syntax error or Table DNE
        except sql.OperationalError as e:
            if ("syntax error" in str(e)):
                raise SyntaxError('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values))
            else:
                raise TableDNE_Error(row, self.getDBName())
        #Constraint violation
        except sql.IntegrityError as e:
            (keys, values) = param.paramTupleDebug(info)
            if ("constraint failed" in str(e)):
                raise ConstraintError('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values), self.getConstraints(row)[0][2], row, self.getDBName())
            else:
                raise UniqueError('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values), self.getConstraints(row)[0][1], row, self.getDBName())
        #Adapter missing
        except sql.InterfaceError as e:
            e = str(e)
            begin = e.find(':')
            end = e.find(' ', begin)
            var_name = e[begin+1:end]
            var_value = info[var_name]
            raise AdapterMissingError(var_value, row, self.getDBName())

    #deleteRow(self,
    #          row,       #Row name
    #          condition) #Condition to select data 
    def deleteRow(self, row, condition):
        query = param.paramKey(condition)
        #print '''DELETE FROM {0} WHERE {1}'''.format(row, query)
        try:
            self.cursor.execute('''DELETE FROM {0} WHERE {1}'''.format(row, query), condition)
            self.db.commit()
            return True
        except sql.OperationalError as e:
            if ("no such table" in str(e)):
                raise TableDNE_Error(row, self.getDBName())
            elif ("no such column" in str(e)):
                e = str(e)
                begin = e.find(':') + 2
                column = e[begin:]
                raise ColumnDNE_Error(column, row, self.getDBName())
            elif ("syntax error" in str(e)):
                query = param.paramDebug(condition)
                raise SyntaxError('''DELETE FROM {0} WHERE {1}'''.format(row, query))

    #getValues(self,
    #          row,       #Row name
    #          info,      #CSV string with columns to retrieve data from
    #          condition) #Dictionary of search requirements
    def getValues(self, row, info, condition):
        query = param.paramKey(condition)
        #print '''SELECT ({0}) FROM {1} WHERE {2}'''.format(info, row, query)
        try:
            self.cursor.execute('''SELECT {0} FROM {1} WHERE {2}'''.format(info, row, query), condition)
            result = self.cursor.fetchall()
            return result
        except sql.OperationalError as e:
            if ("no such column" in str(e)):
                e = str(e)
                begin = e.find(':') + 2
                column = e[begin:]
                raise ColumnDNE_Error(column, row, self.getDBName())
            elif ("syntax error" in str(e)):
                query = param.paramDebug(condition)
                raise SyntaxError('''SELECT ({0}) FROM {1} WHERE {2}'''.format(info, row, query))
            elif ("no such table" in str(e)):
                raise TableDNE_Error(row, self.getDBName())

    #getRow(self,
    #       row,        #Row name
    #       condition)  #Dictionary of data involved in the query
    def getRow(self, row, condition):
        query = param.paramKey(condition)
        #print '''SELECT * FROM {0} WHERE {1}'''.format(row, query)
        try:
            self.cursor.execute('''SELECT * FROM {0} WHERE {1}'''.format(row, query), condition)
            result = self.cursor.fetchall()
            return result
        except sql.OperationalError as e:
            if ("syntax error" in str(e)):
                query = param.paramDebug(condition)
                raise SyntaxError('''SELECT * FROM {0} WHERE {1}'''.format(row, query))
            elif ("no such table" in str(e)):
                raise TableDNE_Error(row, self.getDBName())
            elif ("no such column" in str(e)):
                e = str(e)
                begin = e.find(':') + 2
                column = e[begin:]
                raise ColumnDNE_Error(column, row, self.getDBName())

    #updateRow(self,
    #          row,        #Row name
    #          info,       #Dictionary of new data
    #          condition)  #Dictionary of a single item with a certain value to be found in DB
    def updateRow(self, row, info, condition):
        changes = param.paramDebug(info)
        query = param.paramKey(condition)
        #print '''UPDATE {0} SET {1} WHERE {2}'''.format(row, changes, query)
        try:
            self.cursor.execute('''UPDATE {0} SET {1} WHERE {2}'''.format(row, changes, query), condition)
            self.db.commit()
            return True
        except sql.OperationalError as e:
            if ("syntax error" in str(e)):
                query = param.paramDebug(condition)
                raise SyntaxError('''UPDATE {0} SET {1} WHERE {2}'''.format(row, changes, query))
            elif ("no such table" in str(e)):
                raise TableDNE_Error(row, self.getDBName())
            elif ("no such column" in str(e)):
                e = str(e)
                begin = e.find(':') + 2
                column = e[begin:]
                raise ColumnDNE_Error(column, row, self.getDBName())

    ##getTableNames(self)
    """
    Returns all table names in DB
    """
    def getTableNames(self):
        self.cursor.execute("select * from sqlite_master")
        schema = self.cursor.fetchall()
        tables = []
        for i in schema:
            if (i[0] == "table" and i[1] != "sqlite_sequence"):
                tables.append(str(i[1]))
        return tables

    #getColumnNames(self,
    #               table) #Table name
    """
    Returns all the columns name values from a table
    Returns in the format (tableName, [columnNames])
    """
    def getColumnNames(self, table):
        #Get table header from DB
        d = {'name': table}
        self.cursor.execute("select * from sqlite_master where name=(:name)", d)
        schema = self.cursor.fetchone()
        #Does the table exist?
        if (schema is None):
            raise TableDNE_Error(table, self.getDBName)
        #Find the parenthesis
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

    #getConstraints(self,
    #               table) #Table name
    """
    Returns all the table columns that are under a unique/primary key restraint
    Returns in the format [(table_name, [column info]), ..., (table_name, [column info])]
    """
    def getConstraints(self, table):
        #Get table header from DB
        d = {'name': table}
        self.cursor.execute("select * from sqlite_master where name=(:name)", d)
        schema = self.cursor.fetchone()
        #Does the table exist?
        if (schema is None):
            raise TableDNE_Error(table, self.getDBName)
        #Find the parenthesis
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
        check = []
        for item in columns:
            if (item[1].find('unique') != -1 or item[1].find('primary key') != -1):
                unique.append(item[0])
            elif (item[1].find('check') != -1):
                check.append(item[0])
        return [(name, unique, check)]

    #closeDB(self)
    def closeDB(self):
        try:
            #Save database
            self.db.commit()
            #Close cursor
            self.cursor.close()
            #Close database
            self.db.close()
            return True
        except sql.ProgrammingError:
            raise DBClosedError(self.getDBName())

    #getDBName(self)
    def getDBName(self):
        return self.name

def main():
    db = DB()

    db.closeDB()

if __name__ == '__main__':
    main()
