# -*- coding: utf-8 -*-
from vk_api_functions import send_message, send_image_message, is_member, is_admin
from support_functions import to_cp1251
from game_functions import *



HELP_MESSAGE = '''  Правила игры:
1. Есть 3 конкурирующих команды: Головастики, Утята и Карасики.
2. Вступивший в игру чел зачисляется в ту из команд, в которой на данный момент меньше всего людей.
3. Головастики могут охотиться на Утят, Утята — на Карасиков, а Карасики — на Головастиков.
4. Игрок одной команды (скажем, Головастиков) может написать боту, что какой-то эмсник является членом другой команды (например, Утят). Если он угадает, то команда Головастиков получает один балл, а эмсник, на которого указали боту, выбывает из игры на неделю. Если не угадает, то просто потеряет одну попытку.
5. Если чела спалили, и он выбыл из игры, то через неделю он снова может вступить в игру, и будет зачислен в рандомную команду.
6. У каждого игрока в неделю есть только ДВЕ ПОПЫТКИ(Аутунг, сука, обрати внимание и не трать их бездумно!) угадать члена вражеской команды.
7. Угадывать можно чуваков только из одной конкурирующей команды, зарабатывая баллы.
8. Из игры можно добровольно ливнуть. Ливнувший игрок не сможет возобновить игру до окончания игрового цикла.
9. В конце каждой недели определяется победившая команда, набравшая больше всего баллов.

    Команды управления (без кавычек):
• «game» - справка
• «game start» - начать игру
• «game exit» - выйти из игры
• «game kick id» - попробовать напасть на пользователя, вместо id пишем вкшный id или ник игрока'''

GAME_SCHEMA_IMAGE = 'photo-159851948_456239044'

GS_ANSWERE_TO_BANNED_PLAYER = '''Тебя уже кокнули, малыш)
Подожди до окончания игрового цикла, потом сможешь снова начать играть.'''
GS_ANSWERE_TO_LEAVE_PLAYER = '''Ты уже вышел из игры.
Подожди до окончания игрового цикла, потом сможешь снова начать играть.'''
GS_ANSWERE_TO_ACTIVE_PLAYER = 'Ты уже в игре!'
GS_ANSWERE_TO_NEW_PLAYER = '''Погнали! Теперь ты в игре!
Твоя команда - '''
GS_ANSWERE_TO_ADMIN = 'Админы не играют, сасируй)'
GS_ANSWERE_ABOUT_ENEMIES = '''Твои враги - '''

GE_ANSWERE_TO_NO_PLAYER = 'Чтобы ливнуть из игры, надо сначала ее начать)'
GE_ANSWERE_TO_LEAVE_PLAYER = GS_ANSWERE_TO_LEAVE_PLAYER
GE_ANSWERE_TO_PLAYER = '''Окей, ты покинул игру.
Если захочешь, можешь снова вернуться в нее после начала следующего игрового цикла.'''

GK_ANSWERE_TO_NO_PLAYER = 'Ты еще не начал игру. Чтобы начать, отправь команду «game start».'
GK_ANSWERE_TO_BANNED_PLAYER = GS_ANSWERE_TO_BANNED_PLAYER
GK_ANSWERE_TO_LEAVE_PLAYER = GS_ANSWERE_TO_LEAVE_PLAYER
GK_ANSWERE_ABOUT_NO_USER = 'Пользователя с таким id или ником вообще нет ВК, лол.'
GK_ANSWERE_ABOUT_NO_PLAYER = 'Этот чел еще или уже не в игре. Минус одна попытка)'
GK_ANSWERE_ABOUT_CREWMAN = 'Этот чел из твоей команды. Минус одна попытка)'
GK_ANSWERE_ABOUT_ENEMY = '''Бинго! Ты потратил попытку не зря и выстегнул врага!
Только не хватайся об этом лишний раз, а то тебя раскроют и также выстегнут)'''
GK_ANSWERE_ABOUT_OTHER = '''Этот чел из другой команды, но не из той, на которую охотится твоя команда.
Ты не можешь его атаковать, а вот он тебя может. Ты теряешь одну попытку)'''
GK_ANSWERE_ABOUT_NO_ATTEMPS = '''Ты уже потратил все свои попытки.
Подожди начала следующего игрового цикла. Ну или попробуй прямо сейчас скормить этого чела кому-то из своей команды)'''
GK_ANSWERE_ABOUT_YOURSELF = '''Себя кикнуть не получится)
Если хочешь выйти из игры, юзай команду «game exit»'''

# Функция сортировки полученных сообщений
def sort_message(user):
    message = user['message']
    if message[:4] == 'game':
        if is_member(user['id']):
            if len(message) == 4:
                get_help(user)
            elif message[4] == ' ':
                if message[5:10] == 'start':
                    start_game(user)
                elif message[5:9] == 'exit':
                    exit_game(user)
                elif message[5:9] == 'kick' and len(message) > 10:
                    kick_enemy(user)
                elif message[5:9] == 'help':
                    get_help(user)

def get_help(user):
    send_image_message(user['id'], HELP_MESSAGE, GAME_SCHEMA_IMAGE)

def start_game(user):
#    if is_admin(user['id']):
#        send_message(user['id'], GS_ANSWERE_TO_ADMIN)
#    else:
        state = game_state(user['id'])
        if state == None:
            team = game_min_team()
            game_new_player(user['id'], team)
            team_name = TEAM_NAMES[team]
            enemy_team = TEAM_NAMES[TEAM_ENEMIES[team]]
            send_message(user['id'], GS_ANSWERE_TO_NEW_PLAYER + team_name + '\n' + GS_ANSWERE_ABOUT_ENEMIES + enemy_team)
        elif state == BANNED:
            send_message(user['id'], GS_ANSWERE_TO_BANNED_PLAYER)
        elif state == LEAVE:
            send_message(user['id'], GS_ANSWERE_TO_LEAVE_PLAYER)
        else:
            send_message(user['id'], GS_ANSWERE_TO_ACTIVE_PLAYER)


def exit_game(user):
    state = game_state(user['id'])
    if state == None:
        send_message(user['id'], GE_ANSWERE_TO_NO_PLAYER)
    elif state == LEAVE:
        send_message(user['id'], GE_ANSWERE_TO_LEAVE_PLAYER)
    else:
        game_leave(user['id'])
        send_message(user['id'], GE_ANSWERE_TO_PLAYER)

def kick_enemy(user):
    state = game_state(user['id'])
    if state == None:
        send_message(user['id'], GK_ANSWERE_TO_NO_PLAYER)
    elif state == LEAVE:
        send_message(user['id'], GK_ANSWERE_TO_LEAVE_PLAYER)
    elif state == BANNED:
        send_message(user['id'], GK_ANSWERE_TO_BANNED_PLAYER)
    else:
        if game_attempts(user['id']) < 1:
            send_message(user['id'], GK_ANSWERE_ABOUT_NO_ATTEMPS)
        else:
            target_uid = to_cp1251(user['message'][10:].replace(' ', ''))
            if check_user(target_uid):
                target_uid = get_uid(target_uid)
                if target_uid == user['id']:
                    send_message(user['id'], GK_ANSWERE_ABOUT_YOURSELF)
                else:
                    kick_result = game_attack(user['id'], target_uid)
                    if kick_result == ATTACK_NO_PLAYER:
                        send_message(user['id'], GK_ANSWERE_ABOUT_NO_PLAYER)
                    elif kick_result == ATTACK_CREWMAN:
                        send_message(user['id'], GK_ANSWERE_ABOUT_CREWMAN)
                    elif kick_result == ATTACK_ENEMY:
                        send_message(user['id'], GK_ANSWERE_ABOUT_ENEMY)
                    elif kick_result == ATTACK_OTHER:
                        send_message(user['id'], GK_ANSWERE_ABOUT_OTHER)
            else:
                send_message(user['id'], GK_ANSWERE_ABOUT_NO_USER)




#long_pol(sort_message)
