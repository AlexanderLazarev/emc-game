# -*- coding: utf-8 -*-
# Модуль с функциями для логирования

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

# Логирование ошибок
def log_error(message):
    log(str(message), 'Error')

# Логирование сообщение вк
def log_message(message):
    log(str(message), 'Mess')

# Логирование игровых действий
def log_actions(message):
    log(str(message), 'Action')

# Логирование действий при начале/конце игрового цикла
def log_cicle(message):
    log(str(message), 'Cicle')
