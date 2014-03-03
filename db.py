'''
AUTHOR: COBY JOHNSON
PROJECT: GENERIC --> DATABASE CLASS
LAST UPDATE: 2/17/2014

TODO:
-!!!NEED TO MAKE ALL FUNCTIONS SAFE FROM SQL INJECTION ATTACKS!!!-

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
'''

import sqlite3 as sql

class DB:
    def __init__(self, name):
        #LOAD DATABASE
        self.db = sql.connect(name, detect_types=sql.PARSE_DECLTYPES|sql.PARSE_COLNAMES)
        #CREATE CURSOR
        self.cursor = self.db.cursor()

    #createTable(self,
    #            table, #TABLE NAME
    #            info)  #(COLUMN NAME 1, ..., COLUMN NAME X)
    def createTable(self, table, info):
        self.cursor.execute('''CREATE TABLE {0}{1}'''.format(table, info))
        self.db.commit()
        return
        
    #dropTable(self,
    #          table) #TABLE NAME
    def dropTable(self, table):
        self.cursor.execute('''DROP TABLE IF EXISTS {0}'''.format(table))
        self.db.commit()
        return

    #alterTable(self,
    #           table,   #TABLE NAME
    #           command) #SUPPORTS ADD column, RENAME TO table
    ### NOTE: SQLITE3 DOES NOT SUPPORT: RENAME column, DROP column ###
    def alterTable(self, table, command):
        #print 'ALTER TABLE {0} {1}'.format(table, command)
        self.cursor.execute('''ALTER TABLE {0} {1}'''.format(table, command))
        self.db.commit()
        return

    #insertRow(self,
    #          row,  #ROW NAME
    #          info) #(INFO 1, ..., INFO X)
    def insertRow(self, row, info):
        try:
            keys = ""
            values = ""
            for k in info.keys():
                keys += k + ", "
                values += ":" + k + ", "
            keys = keys[:len(keys)-2]
            values = values[:len(values)-2]
            
            print '''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values)
            self.cursor.execute('''INSERT INTO {0} ({1}) VALUES ({2})'''.format(row, keys, values), info)
            
            #print '''INSERT INTO {0} VALUES{1}'''.format(row, info)
            #self.cursor.execute('''INSERT INTO {0} VALUES {1}'''.format(row, info))
            self.db.commit()
            return
        except sql.IntegrityError:
            ### ||| NOTE: MODIFY THIS EXCEPTION FOR YOUR DB SPECIFICALLY ||| ###
            ### \\\                                                      /// ###
            print '##### Duplicate value in table with unique restraint. #####'
            temp = info.split()
            current = self.getRow(row, 'name={0}'.format(temp[0].strip("(,)")))
            response = raw_input('Do you want to merge --> {0},\n    with this record --> {1}\n (Y/n)?'.format(info, current))
            if (response == 'N' or response == 'n'):
                print 'Record discarded'
            else:
                num = int(temp[2].strip(','))
                self.updateRow('MTG', 'count', current[2] + num, current[3])
                self.db.commit()
            ### ///                                                      \\\ ###
            ### ||| NOTE: MODIFY THIS EXCEPTION FOR YOUR DB SPECIFICALLY ||| ###
        
    #deleteRow(self,
    #          row,       #ROW NAME
    #          condition) #INSERT CONDITIONAL STATEMENT   
    def deleteRow(self, row, condition):
        #print '''DELETE FROM {0} WHERE {1}'''.format(row, condition)
        self.cursor.execute('''DELETE FROM {0} WHERE {1}'''.format(row, condition))
        self.db.commit()
        return

    #getRowByID(self,
    #           row,  #ROW NAME
    #           ID)   #ID OF ROW TO RETURN
    def getRowByID(self, row, ID):
        #print '''SELECT * FROM {0} WHERE ID={1}'''.format(row, ID)
        self.cursor.execute('''SELECT * FROM {0} WHERE ID=?'''.format(row), (ID))
        result = self.cursor.fetchone()
        if (result == None):
            print '##### No data from table "{0}" exists with ID "{1}" #####'.format(row, ID)
        return result

    #getRow(self,
    #           row,       #ROW NAME
    #           condition) #ID OF ROW TO RETURN
    def getRow(self, row, condition):
        print '''SELECT * FROM {0} WHERE {1}'''.format(row, condition)
        self.cursor.execute('''SELECT * FROM {0} WHERE {1}'''.format(row, condition))
        result = self.cursor.fetchone()
        if (result == None):
            print '##### No data from table "{0}" exists with statement "{1}" #####'.format(row, condition)
        return result

    #updateRow(self,
    #          row,    #ROW NAME
    #          column, #COLUMN NAME
    #          value,  #NEW COLUMN VALUE
    #          ID)     #ID OF ROW
    def updateRow(self, row, column, value, ID):
        print '''UPDATE {0} SET {1}={2} WHERE ID={3}'''.format(row, column, value, ID)
        self.cursor.execute('''UPDATE {0} SET {1}=? WHERE ID=?'''.format(row, column), (value, ID))
        self.db.commit()
        return

    #innerJoin(self,
    #          table1,    #
    #          column1,   #
    #          table2,    #
    #          column2,   #
    #          condition) #
    #
    def innerJoin(self, table1, column1, table2, column2, condition):
        print '''SELECT {0}.{1}, {2}.{3} FROM {0} JOIN {2} ON {4}'''.format(table1, column1, table2, column2, condition)
        self.cursor.execute('''SELECT {0}.{1}, {2}.{3} FROM {0} JOIN {2} ON {4}'''.format(table1, column1, table2, column2, condition))
        results = self.cursor.fetchall()
        return results

    #printTable(self,
    #           table) #TABLE NAME
    def printTable(self, table):
        cursor = self.cursor.execute('''SELECT * FROM {0}'''.format(table))
        for row in cursor:
            print row
        return

    #getColumnNames(self,
    #               table) #TABLE NAME
    def getColumnNames(self, table):
        try:
            self.db.row_factory = sql.Row
            cursor = self.db.execute('select * from {0}'.format(table))
            row = cursor.fetchone()
            names = row.keys()
            return tuple(names)
        except:
            print '##### No columns in table "{0}". #####'.format(table)
            return ()

    #closeDB(self)
    def closeDB(self):
        #SAVE DATABASE
        self.db.commit()
        #CLOSE CURSOR
        self.cursor.close()
        #CLOSE DATABASE
        self.db.close()
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

    hack = "ilovehackers@hackers.net"
    print db.safe(hack)
    hack = "anything' or 'x'='x'"
    print db.safe(hack)
    hack = "steve@unixwiz.net'"
    print db.safe(hack)
    hack = "x' AND email IS NULL; --"
    print db.safe(hack)
    hack = "x' AND 1=(SELECT COUNT(*) FROM tabname); --"
    print db.safe(hack)
    hack = "x' AND members.email IS NULL; --"
    print db.safe(hack)

    db.dropTable('MTG')

    db.createTable('MTG', '(name TEXT UNIQUE, color TEXT, count INTEGER, ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT)')
    db.insertRow('MTG', {'name': 'Plain', 'color': 'WH', 'count': 50, 'ID': None})
    db.insertRow('MTG', "('Swamp', 'BK', 50, NULL)")
    db.insertRow('MTG', "('Swamp', 'BK', 50, NULL)")

    db.printTable('MTG')
    
    db.closeDB()

main()
