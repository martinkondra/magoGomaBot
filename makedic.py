import pickle
import codecs
from silabeador import Silabeo, has_vowels

def insertIntoDict(d,key,value):
    if not key in d:
        d[key] = [value]
    else:
        d[key].append(value)

all_words = []
words = []
d = {}
d_all = {}
with codecs.open("10mil.txt", "r", "ISO-8859-1") as txt:
    for line in txt:
        word = line.split()[1]
        if len(word)==1 or has_vowels(word)==False:
            print("BAD WORD", word)
        else:
            print(word),
            try:
                first = Silabeo.parse(word)[0]
                last = Silabeo.parse(word)[-1]
                print(first, last)
                insertIntoDict(d, first, word)
                words.append(word)
            except:
                continue
    pickle.dump(d, open('dicc.p', "wb"))
    pickle.dump(words, open('words.p', "wb"))
    print(d['la'])

'''
with codecs.open("CREA_total.txt", "r", "ISO-8859-1") as txt:
    for line in txt:
        word = line.split()[1]
        all_words.append(word)
    pickle.dump(all_words, open('all_words.p', "wb"))
'''
with codecs.open("CREA_total.txt", "r", "ISO-8859-1") as txt:
    for line in txt:
        word = line.split()[1]
        if len(word)==1 or has_vowels(word)==False:
            print("BAD WORD", word)
        else:
            try:
                first = Silabeo.parse(word)[0]
                last = Silabeo.parse(word)[-1]
                print(first, last)
                insertIntoDict(d_all, first, word)
                words.append(word)
            except:
                continue
    pickle.dump(d_all, open('dicc_all_words.p', "wb"))
    pickle.dump(words, open('all_words.p', "wb"))
    print(d_all['la'])
