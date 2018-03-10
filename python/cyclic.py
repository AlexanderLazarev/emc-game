# -*- coding: utf-8 -*-
# Модуль, запускаемый с заданной переодичностью (по умолчанию - раз в неделю)
from vk_api_functions import auth, send_message, post
from game_functions import game_clean_bans, game_clean_leave, game_clean_scores, game_winners, game_get_banned
from constants import TEAM_NAMES, TEAM_PICTURES
from log_functions import log_cicle

WIN_MESS = 'Игровая неделя подошла к концу. \nВ этот раз больше всего баллов набрала команда - '
WIN_GRAC_MESS = '\nГрац их!'
END_MESS = '\n\n(Не понимаешь, чоза игра такая? Напиши слово «game» в лс группы, и узнаешь))'
DRAW_MESS = 'Игровая неделя подошла к концу. \nВ этот раз одинаковое кол-во баллов набрали команды - '
DRAW_GRAC_MESS = '\nБудем считать, что победила дружба)'
MESS_TO_BANNED = '''Начался новый игровой цикл, и теперь ты можешь снова вступить в игру.
Для этого достаточно отправить команду «game start» в личку группы'''

log_cicle('КОНЕЦ ИГРОВОГО ЦИКЛА!')
auth()
ban_list = game_get_banned()
winners = game_winners()
game_clean_bans()
game_clean_leave()
game_clean_scores()
if len(winners) == 1:
    post(WIN_MESS + TEAM_NAMES[winners[0]] + WIN_GRAC_MESS + END_MESS, TEAM_PICTURES[winners[0]])
else:
    pictures_str = TEAM_PICTURES[winners[0]] + ',' + TEAM_PICTURES[winners[1]]
    if len(winners) == 2:
        winners_str = TEAM_NAMES[winners[0]] + ' и ' + TEAM_NAMES[winners[1]]
    else:
        winners_str = TEAM_NAMES[winners[0]] + ', ' + TEAM_NAMES[winners[1]] + ' и ' + TEAM_NAMES[winners[2]]
        pictures_str += ',' + TEAM_PICTURES[winners[2]]
    post(DRAW_MESS + winners_str + DRAW_GRAC_MESS + END_MESS, pictures_str)
for player in ban_list:
    send_message(player[0], MESS_TO_BANNED)

log_cicle('НАЧАЛО ИГРОВОГО ЦИКЛА!')
