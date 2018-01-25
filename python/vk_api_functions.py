# -*- coding: utf-8 -*-
# Мудуль с функциями для работы с api вк

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import unicodedata
from constants import ID_APP, PROJECT_DIR, SKOPE, GROUP_ID
from log_functions import log, error
from support_functions import to_cp1251

# Авторизация вк
def auth():
    result = True
    try:
        global vk_api_u, vk_api_g, group_session
        auth_data = open(PROJECT_DIR + "auth-data", 'r')
        user_token = auth_data.readline()
        user_token = user_token[0:len(user_token)-1]
        group_token = auth_data.readline()
        group_token = group_token[0:len(group_token)-1]
        auth_data.close()
        group_session = vk_api.VkApi(token=group_token)
        user_session = vk_api.VkApi(token=user_token)
        vk_api_g = group_session.get_api()
        vk_api_u = user_session.get_api()
        log('User authorization successful!')
    except Exception as e:
        error(e)
        result = False
    return result

# Проверка, есть ли такой юзер вк
def check_user(user_nick):
    try:
        vk_api_u.users.get(user_ids=user_nick)
        return True
    except:
        return False

# Получения id юзера по его нику
def get_uid(user_nick):
    try:
        result = vk_api_u.users.get(user_ids=user_nick)[0]['id']
    except:
        result = False
    return result

# Получение кортежа с id, именем и фамилией юзера
def get_user(user_nick):
    try:
        result = vk_api_u.users.get(user_ids=user_nick, fields='id,first_name,last_name')[0]
    except:
        result = False
    return result

# Проверка, является ли юзер членом группы
def is_member(user_id):
    if vk_api_u.groups.isMember(group_id=GROUP_ID, user_id=user_id):
        return True
    else:
        return False

# Проверка, является ли юзер админом группы
def is_admin(user_id):
    admins = vk_api_g.groups.getMembers(group_id=GROUP_ID, fields='first_name', filter='managers')['items']
    result = False
    for user in admins:
        uid = user['id']
        if user_id == uid:
            result = True
            break
    return result

# Отправка сообщения юзеру от лица группы
def send_message(user_id, message):
    message = str(message)
    send_message = message.decode('utf8')
    vk_api_g.messages.send(user_id=user_id, message=send_message)
    log('Отправлено сообщение: ' + message)


# Постинг на стене группы
def post(message):
    message = str(message)
    message = message.decode('utf8')
    print(vk_api_u.wall.post(owner_id=-GROUP_ID, message=message,from_group=1))

# Функция получения сообщений
def long_pol(function):
    longpoll = VkLongPoll(group_session)
    for event in longpoll.listen():
        if event.to_me:
            message = event.text
            log('Получено сообщение: ' + to_cp1251(message))
            user = get_user(event.user_id)
            user.update({'message' : message})
            function(user)
