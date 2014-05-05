"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/4/2014
VERSION: 0.0.1

DONE:

TODO:
[V 0.0.1]
    - Log to console or file

"""
import datetime

class Logger:

    def __init__(self, output):
        if (output == 'console'):
            self.output = 'console'
        elif (output == 'file'):
            self.output = 'file'
            self.f_name = 'LOG_' + str('@'.join(str(datetime.datetime.now()).replace(':', '.').split()))[:-7] + '.lgf'
        else:
            self.output = 'console'
            self.note('! ({0}) is not a valid choice.\n! Please use "console" or "file".\n! Logging set to be done in console.'.format(output))

        self.note('START: ' + str(datetime.datetime.now()) + '\n')

    def __del__(self):
        self.note('\n' + 'DONE:  ' + str(datetime.datetime.now()) + '\n')

    def note(self, text):
        if (self.output == 'console'):
            print text
        elif (self.output == 'file'):
            fo = open(self.f_name, 'a')
            fo.write(text + '\n')
            fo.close()

def main():
    t = Logger('file')

if __name__ == '__main__':
    main()