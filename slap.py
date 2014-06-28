"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 6/27/2014
VERSION: 0.2.4

== Constructors / Destructors ==
+ DB.init (5/4/2014)
+ DB.del (6/27/2014)

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

- [V 0.2.5] - Alter Table
    - Make an alterTable method
        ? Extend the functionality to allow renaming tables and dropping tables if possible

- [V 0.2.6] - Join Table
    ? Is if practical to make generic join statements
    - Outer join
    - Inner join

"""

from errors import *
import logger as log
import parameterize as param
import sqlite3 as sql

class DB:
    #__int__(self,
    #        name,     #Name of the DB to be created
    #        keep_log) #Enter 'console' or 'file' as destination to write a log
    def __init__(self, name=":memory:", log_commands="No"):
        #Logger
        if (log_commands is not "No"):
            self.keep_log = True
            self.record = log.Logger(log_commands)
        else:
            self.keep_log = False

        #Name
        i = name.rfind('.')
        if (i != -1):
            self.name = name[:i]
        else:
            self.name = name

        #Load DB
        self.db = sql.connect(name)
        if (self.keep_log):
            self.record.note('''Open DB ({0})'''.format(self.getDBName()))
        #Create DB cursor
        self.cursor = self.db.cursor()
        if (self.keep_log):
            self.record.note('''Open cursor''')

    #__del__(self)
    def __del__(self):
        try:
            del self.record
            del self.keep_log
            del self.name
            del self.db
            del self.cursor
        finally:
            return True

    #createTable(self,
    #            table, #Table name
    #            info)  #(Column_name_1, ..., Column_name_X)
    def createTable(self, table, info):
        if (self.keep_log):
            self.record.note('''CREATE TABLE {0} {1}'''.format(table, info))
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
        if (self.keep_log):
            self.record.note('''DROP TABLE IF EXISTS {0}'''.format(table))
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
        if (self.keep_log):
            self.record.note('''DELETE FROM {0}'''.format(table))
        try:
            self.cursor.execute('''DELETE FROM {0}'''.format(table))
            self.db.commit()
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
        if (self.keep_log):
            (tk, tv) = param.paramTupleDebug(info)
            self.record.note('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, tk, tv))
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
        (query, clean) = param.paramKey(condition)
        if (self.keep_log):
            tq = param.paramDebug(condition)
            self.record.note('''DELETE FROM {0} WHERE {1}'''.format(row, tq))
        try:
            self.cursor.execute('''DELETE FROM {0} WHERE {1}'''.format(row, query), clean)
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
        (query, clean) = param.paramKey(condition)
        if (self.keep_log):
            tq = param.paramDebug(condition)
            self.record.note('''SELECT ({0}) FROM {1} WHERE {2}'''.format(info, row, tq))
        try:
            self.cursor.execute('''SELECT {0} FROM {1} WHERE {2}'''.format(info, row, query), clean)
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
        (query, clean) = param.paramKey(condition)
        if (self.keep_log):
            tq = param.paramDebug(condition)
            self.record.note('''SELECT * FROM {0} WHERE {1}'''.format(row, tq))
        try:
            self.cursor.execute('''SELECT * FROM {0} WHERE {1}'''.format(row, query), clean)
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
        (query, clean) = param.paramKey(condition)
        if (self.keep_log):
            tq = param.paramDebug(condition)
            self.record.note('''UPDATE {0} SET {1} WHERE {2}'''.format(row, changes, tq))
        try:
            self.cursor.execute('''UPDATE {0} SET {1} WHERE {2}'''.format(row, changes, query), clean)
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

    #getTableNames(self)
    # Return all table names in db
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
    # Returns all the columns name values from a table
    # in the format (tableName, [columnName0, ..., columnNameX])
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
        #Splice out the column names
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
    # Returns all the table columns that are under a unique/primary key restraint
    # in the format [(table_name, [column info]), ..., (table_name, [column info])]
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
        #Splice out the column names
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
            if (self.keep_log):
                self.record.note('''Close cursor''')
            #Close database
            self.db.close()
            if (self.keep_log):
                self.record.note('''Close DB ({0})'''.format(self.getDBName()))
            return True
        except sql.ProgrammingError:
            raise DBClosedError(self.getDBName())

    #getDBName(self)
    def getDBName(self):
        return self.name

def main():
    db = DB(name='test.sql', log_commands='console')
    db.createTable('test', '(name TEXT, ID INTEGER NOT NULL PRIMARY KEY)')
    db.insertRow('test', {'name': 'Coby'})
    db.insertRow('test', {'name': 'Keely'})
    db.insertRow('test', {'name': 'Chancie'})
    db.insertRow('test', {'name': 'Misty'})
    db.insertRow('test', {'name': 'Dusty'})
    #print db.getValues('test', 'ID', {'name': 'Coby'})
    #print db.getRow('test', {'ID': ('>=', 1)})
    db.deleteRow('test', {'name': 'Dusty'})
    #print db.getRow('test', {'ID': ('>=', 1)})
    db.updateRow('test', {'name': 'OOPS!'}, {'ID': ('>=', 1)})
    #print db.getRow('test', {'ID': ('>=', 1)})

    db.clearTable('test')
    db.dropTable('test')

    db.closeDB()

if __name__ == '__main__':
    main()
