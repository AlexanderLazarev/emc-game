# -*- coding: utf-8 -*-

import sqlite3

from constants import *


#Проверено
def db_get_request(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(request)
    result = cursor.fetchall()
    conn.close()
    return result

#Проверено
def db_set_request(request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(request)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

#Проверено
def db_get_state(uid):
    request = db_get_request('SELECT state FROM users WHERE _id=' + str(uid))
    if request == []:
        result = None
    else:
        result = request[0][0]
    return result

def db_get_attempts(uid):
    return db_get_request('SELECT attempt FROM users WHERE _id=' + str(uid))[0][0]

#Проверено
def db_set_state(uid, state):
    db_set_request('UPDATE users SET state=' + str(state) + ', attempt=0 WHERE _id=' + str(uid))

#Проверено
def db_add_user(uid, state):
    return db_set_request('INSERT INTO users (_id, state, attempt) VALUES (' + str(uid) + ', ' + str(state) + ', ' + str(MAX_ATTEMPS) + ')')

#Проверено
def db_del_user(uid):
    return db_set_request('DELETE FROM users WHERE _id=' + str(uid))

def db_get_bans():
    return db_get_request('SELECT _id FROM users WHERE state = ' + str(BANNED))

def db_clean_bans():
    db_set_request('DELETE FROM users WHERE state=' + str(BANNED))

def db_clean_leave():
    db_set_request('DELETE FROM users WHERE state=' + str(LEAVE))

#Проверено
def db_get_min_team():
    green = db_get_request('SELECT COUNT(_id) FROM users WHERE state=' + str(1))[0][0]
    yellow = db_get_request('SELECT COUNT(_id) FROM users WHERE state=' + str(2))[0][0]
    red = db_get_request('SELECT COUNT(_id) FROM users WHERE state=' + str(3))[0][0]
    Min = min([green, yellow, red])
    if Min == green:
        return TEAM_GREEN_NUM
    if Min == yellow:
        return TEAM_YELLOW_NUM
    if Min == red:
        return TEAM_RED_NUM

#Проверено
def db_minus_attempt(uid):
    return db_set_request('UPDATE users SET attempt=(SELECT attempt FROM users WHERE _id=' + str(uid) + ')-1 WHERE _id=' + str(uid))

# Получение счета команд
def db_get_scores():
    return db_get_request('SELECT score FROM results ORDER BY team_number')

# Очистить счет команд
def db_clean_scores():
    db_set_request('UPDATE results SET score=0')
