"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 10/22/2016
VERSION: 0.0.2

== Constructors / Destructors ==
+ Logger.init (6/27/2014)
+ Logger.del (7/14/2014)

== Methods ==
+ Logger.note (6/27/2014)

TODO:
- [V 0.0.3]

"""
import datetime
import os

class Logger:

    def __init__(self, output):
        if (output == 'console'):
            self.output = 'console'
        elif (output == 'file'):
            self.output = 'file'
            path = os.getcwd()+'\\logs'
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            file_name = 'LOG_' + str('@'.join(str(datetime.datetime.now()).replace(':', '.').split()))[:-10] + '.txt'
            self.file = open(path+'\\'+file_name, 'a')
        else:
            self.output = 'console'
            self.note('! ({0}) is not a valid choice.\n! Please use "console" or "file".\n! Logging set to be done in console.'.format(output))

        self.note('START: ' + str(datetime.datetime.now()) + '\n')

    def __del__(self):
        self.note('\n' + 'DONE:  ' + str(datetime.datetime.now()) + '\n')
        if (self.output == 'file'):
            self.file.close()

    def note(self, text):
        if (self.output == 'console'):
            print(text)
        elif (self.output == 'file'):
            self.file.write(text + '\n')

def main():
    t = Logger('file')

if __name__ == '__main__':
    main()