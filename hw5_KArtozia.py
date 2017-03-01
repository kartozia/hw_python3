import json

mystem = open('', 'r', encoding='utf-8')
text = mystem.read()
dictionary = json.loads(text)


##class Word:
##    def __init__(self, form, variant, lemma, pos):
##        self.word = form
##        self.var = variant
##        self.freq_lemma = lemma
##        self.freq_pos = pos
