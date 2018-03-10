# -*- coding: utf-8 -*-
# Главный модуль

from message_processing import sort_message
from vk_api_functions import long_pol, auth

auth()
long_pol(sort_message)
