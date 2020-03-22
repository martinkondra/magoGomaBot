# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import random
import unidecode
from nuevosilabeador import silabeador

all_words = pickle.load(open("all_words.p", "rb"))
#words = pickle.load(open("all_words.p", "rb"))
words = pickle.load(open("words.p", "rb"))
#d = pickle.load(open("dicc_all_words.p", "rb"))
d = pickle.load(open("dicc.p", "rb"))

def validate(word, current_syl, used):
    print(current_syl)
    if word in used:
        print('Perdiste! Esa palabra ya fue usada.')
        return 'used'
    if word_exists(word) == False:
        return 'notword'
    used.append(word)
    word = replace_accents(word)
    first = get_first(word)
    print('validating ', first, current_syl)
    if first==current_syl and len(silabeador(word))>1:
        #print('validate:', current_syl)
        return True
    else:
        print('Perdiste!')
        return False

def choose_word(current_syl):
    if not current_syl in d:
        print('Ganaste! Envia /start para la revencha.')
        return False
    candidates = (d[current_syl])
    if candidates:
        return random.choice(candidates)
    else:
        return False
    ''' Con lo que sigue, el bot solo elige palabras que tengan una posible respuesta
    while True:
        candidate = random.choice(candidates)
        #print(candidate)
        last = get_last(candidate)
        if d.get(last) and len(silabeador(candidate))>1:
            return candidate
    return False
    '''

def get_last(word):
    splitted = silabeador(word)
    last = str(splitted[-1])
    last = replace_accents(last)
    return last


def get_first(word):
    splitted = silabeador(word)
    first = str(splitted[0])
    first = replace_accents(first)
    return first

def word_exists(word):
    if word in all_words:
        return True
    else:
        return False

def replace_accents(word):
    return unidecode.unidecode(word)