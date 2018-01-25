# -*- coding: utf-8 -*-
from vk_api_functions import auth, long_pol, send_message
from support_functions import to_cp1251

# Функция сортировки полученных сообщений
def sort_message(user):
    message = user['message']
    print(message)
#    print '3 - ' + message[3]
#    print '4 - ' + message[4]
#    print '5 - ' + message[5]
    if message[:4] == 'game':
        if len(message) == 4:
            get_help(user)
        elif message[4] == ' ':
            if message[5:10] == 'start':
                start_game(user)
            elif message[5:9] == 'exit':
                exit_game(user)
            elif message[5:9] == 'kick':
                kick_enemy(user)

def get_help(user):
    send_message(user['id'], "Хелп еще не написан, " + to_cp1251(user['first_name']))

def start_game(user):
    send_message(user['id'], to_cp1251(user['first_name']) + ' начал игру')

def exit_game(user):
    send_message(user['id'], to_cp1251(user['first_name']) + ' вышел из игры')

def kick_enemy(user):
    print('kick')

auth()
long_pol(sort_message)
