# Module with secondary functions

import datetime
from constants import LOG_DIR

def log(message, prefix = 'Main'):
    prefix = '[' + prefix + ']'
    now = datetime.datetime.today()
    date = now.strftime("%m.%d.%Y")
    time = now.strftime("%H:%M:%S")
    log_file = open(LOG_DIR + 'log_' + date, 'a')
    output = '[' + date + '-' + time + ']' + prefix + ' ' + message + '\n'
    log_file.write(output)
    print output
    log_file.close()

def error(message):
    log(str(message), 'Error')
