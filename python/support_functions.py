# -*- coding: utf-8 -*-
import unicodedata


def to_cp1251(text):
    return text.encode('utf8', 'cp1251')
