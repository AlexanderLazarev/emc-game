# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from database_functions import *
from log_functions import log_actions, log_cicle
from support_functions import to_cp1251

def game_state(uid):
    return db_get_state(uid)

def game_attempts(uid):
    return db_get_attempts(uid)

def game_get_banned():
    return db_get_bans()

def game_ban(uid):
    db_set_state(uid, BANNED)
    log_actions('Игрок ' + str(uid) + ' был кикнут')

def game_leave(uid):
    db_set_state(uid, LEAVE)
    log_actions('Игрок ' + str(uid) + ' покинул игру')

def game_clean_bans():
    db_clean_bans()
    log_cicle('Список банов очищен')

def game_clean_leave():
    db_clean_leave()
    log_cicle('Список вышедших игроков очищен')

def game_attack(uid_attack, uid_target):
    state_target = db_get_state(uid_target)
    if state_target == 0 or state_target == 10 or state_target == None:
        result = ATTACK_NO_PLAYER
    else:
        state_attack = db_get_state(uid_attack)
        if state_attack == state_target:
            result = ATTACK_CREWMAN
        elif TEAM_ENEMIES[state_attack] == state_target:
            game_ban(uid_target)
            result = ATTACK_ENEMY
        else:
            result = ATTACK_OTHER
    game_minus_attempt(uid_attack)
    return result

def game_min_team():
    return db_get_min_team()

def game_new_player(uid, team):
    db_add_user(uid, team)
    log_actions('Игрок ' + str(uid) + ' начал игру')

def game_minus_attempt(uid):
    db_minus_attempt(uid)
    log_actions('Игрок ' + str(uid) + ' потратил одну попытку')

def game_scores():
    return db_get_scores()

def game_winners():
    scores = game_scores()
    winners = []
    if scores[TEAM_GREEN_NUM-1][0] >= scores[TEAM_RED_NUM-1][0] and scores[TEAM_GREEN_NUM-1][0] >= scores[TEAM_YELLOW_NUM-1][0]:
        winners.append(TEAM_GREEN_NUM)
    if scores[TEAM_YELLOW_NUM-1][0] >= scores[TEAM_GREEN_NUM-1][0] and scores[TEAM_YELLOW_NUM-1][0] >= scores[TEAM_RED_NUM-1][0]:
        winners.append(TEAM_YELLOW_NUM)
    if scores[TEAM_RED_NUM-1][0] >= scores[TEAM_GREEN_NUM-1][0] and scores[TEAM_RED_NUM-1][0] >= scores[TEAM_YELLOW_NUM-1][0]:
        winners.append(TEAM_RED_NUM)
    return winners


def game_clean_scores():
    db_clean_scores()
    log_cicle('Результаты команд сброшены')
