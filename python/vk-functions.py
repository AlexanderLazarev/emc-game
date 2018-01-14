# -*- coding: utf-8 -*-
# Module with functions for working with VK API

import vk_api
import unicodedata
from vk_api.longpoll import VkLongPoll, VkEventType
from constants import ID_APP, PROJECT_DIR, SKOPE, GROUP_ID
from log_functions import log, error


# Authorization in VK
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

# Group-authorization in VK


# Check if is vk user
def check_user(user_nick):
    try:
        vk_api_u.users.get(user_ids=user_nick)
        return True
    except:
        return False

# Getting user-id by user-nickname
def get_uid(user_nick):
    try:
        result = vk_api_u.users.get(user_ids=user_nick)[0]['id']
    except:
        result = False
    return result

def get_user(user_nick):
    try:
        result = vk_api_u.users.get(user_ids=user_nick, fields='id,first_name,last_name')[0]
    except:
        result = False
    return result

# Check if the user is a member of group
def is_member(user_id):
    if vk_api_u.groups.isMember(group_id=GROUP_ID, user_id=user_id):
        return True
    else:
        return False

# Check if the user is an admin
def is_admin(user_id):
    admins = vk_api_g.groups.getMembers(group_id=GROUP_ID, fields='first_name', filter='managers')['items']
    result = False
    for user in admins:
        uid = user['id']
        if user_id == uid:
            result = True
            break
    return result

# Send message from group to user
def send_message(user_id, message):
    message = message.encode('utf8')
    vk_api_g.messages.send(user_id=user_id, message=message)
    log('Отправлено сообщение: ' + message)


# Post on group wall
def post(message):
    message = message.decode('utf8')
    print vk_api_u.wall.post(owner_id=-GROUP_ID, message=message,from_group=1)

def long_pol():
    longpoll = VkLongPoll(group_session)
    for event in longpoll.listen():
        if event.to_me:
            uid = event.user_id
            print uid
            print get_user(uid)
            send_message(event.user_id, get_user(uid)['first_name'])


auth()
long_pol()
#long_pol_server()
#long_pol_history()
