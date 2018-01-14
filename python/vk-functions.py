# -*- coding: utf-8 -*-
# Module with functions for working with VK API

import vk
from constants import ID_APP, PROJECT_DIR, SKOPE, GROUP_ID
from log_functions import log, error


# Authorization in VK
def auth():
    result = True
    try:
        auth_data = open(PROJECT_DIR + "auth-data", 'r')
        login = auth_data.readline()
        login = login[0:len(login)-1]
        password = auth_data.readline()
        password = password[0:len(password)-1]
        token = auth_data.readline()
        token = token[0:len(token)-1]
        auth_data.close()
        user_session = vk.AuthSession(ID_APP, login, password, SKOPE)
        group_session = vk.AuthSession(access_token=token)
        global vk_api_u, vk_api_g
        vk_api_u = vk.API(user_session)
        vk_api_g = vk.API(group_session)
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
        result = vk_api_u.users.get(user_ids=user_nick)[0]['uid']
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
    admins = vk_api_u.groups.getMembers(group_id=GROUP_ID, fields='first_name', filter='managers')['users']
    result = False
    for user in admins:
        uid = user['uid']
        if user_id == uid:
            result = True
            break
    return result

# Send message from group to user
def send_message(user_id, message):
    try:
        vk_api_g.messages.send(user_id=user_id, message=message)
        log('Отправлено сообщение: ' + message)
    except Exception as e:
        error(e)

# Post on group wall
def post(message):
    vk_api_u.wall.post(owner_id=-GROUP_ID, message=message,from_group=1)

def long_pol_server():
    try:
        LP_data = vk_api_u.messages.getLongPollServer(need_pts=1)
        global ts, pts
        ts = int(LP_data['ts'])
        pts = int(LP_data['pts'])
        print ts
        print pts
        return True
    except Exception as e:
        error(e)
        return False

def long_pol_history():
    history = vk_api_u.messages.messages.getLongPollHistory(ts=int(ts), pts=int(pts), max_msg_id=1, version=5.69)
    print history

auth()
long_pol_server()
long_pol_history()
