# -*- coding: utf-8 -*-
# Модуль с глобальными константами

global ID_APP
global PROJECT_DIR
global LOG_DIR
global DB_PATH
global SKOPE
global GROUP_ID
global TOKEN

# Команда головастиков (зеленые)
global TEAM_GREEN_NUM
global TEAM_GREEN_NAME
global TEAM_GREEN_ENEMY
global TEAM_GREEN_PIC
# Команда утят (желтые)
global TEAM_YELLOW_NUM
global TEAM_YELLOW_NAME
global TEAM_YELLOW_ENEMY
global TEAM_YELLOW_PIC
# Команда карасиков (красные)
global TEAM_RED_NUM
global TEAM_RED_NAME
global TEAM_RED_ENEMY
global TEAM_RED_PIC

# Словарь названий команд
global TEAM_NAMES
# Словарь врагов команд
global TEAM_ENEMIES
# Словарь картинок команд
global TEAM_PICTURES

# Атака на не-игрока
global ATTACK_NO_PLAYER
# Атака противника
global ATTACK_ENEMY
# Атака члена команды
global ATTACK_CREWMAN

# Максимальное число попыток в неделю
global MAX_ATTEMPS
# Продолжительность одного игрового цикла в днях
global GAME_CYCLE
# Номер состояния забаненного
global BANNED
# Номер состояния вышедшего из игры
global LEAVE

ID_APP = 6002097
GROUP_ID = 159851948
PROJECT_DIR = "/home/alex/emc-game/"
LOG_DIR = PROJECT_DIR + '/logs/'
DB_PATH = PROJECT_DIR + '/database.db'
SKOPE = 'wall, messages, groups, users, photos'

TEAM_GREEN_NUM = 1
TEAM_GREEN_NAME = 'Головастики'
TEAM_YELLOW_NUM = 2
TEAM_YELLOW_NAME = 'Утята'
TEAM_RED_NUM = 3
TEAM_RED_NAME = 'Карасики'

TEAM_GREEN_ENEMY = TEAM_YELLOW_NUM
TEAM_YELLOW_ENEMY = TEAM_RED_NUM
TEAM_RED_ENEMY = TEAM_GREEN_NUM

TEAM_GREEN_PIC = 'photo-159851948_456239046'
TEAM_YELLOW_PIC = 'photo-159851948_456239045'
TEAM_RED_PIC = 'photo-159851948_456239047'

TEAM_NAMES = {TEAM_RED_NUM:TEAM_RED_NAME, TEAM_GREEN_NUM:TEAM_GREEN_NAME, TEAM_YELLOW_NUM:TEAM_YELLOW_NAME}
TEAM_ENEMIES = {TEAM_RED_NUM:TEAM_RED_ENEMY, TEAM_GREEN_NUM:TEAM_GREEN_ENEMY, TEAM_YELLOW_NUM:TEAM_YELLOW_ENEMY}
TEAM_PICTURES = {TEAM_RED_NUM:TEAM_RED_PIC, TEAM_GREEN_NUM:TEAM_GREEN_PIC, TEAM_YELLOW_NUM:TEAM_YELLOW_PIC}

MAX_ATTEMPS = 2
GAME_CYCLE = 7
BANNED = 0
LEAVE = 10

ATTACK_NO_PLAYER = 10
ATTACK_ENEMY = 11
ATTACK_CREWMAN = 12
ATTACK_OTHER = 13

# EMC constants
#GROUP_ID = 65590361

#TEST_ID = 159851948
