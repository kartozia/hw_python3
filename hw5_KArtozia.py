import json 

mystem = open('python_mystem.json', 'r', encoding='utf-8')
text = mystem.readlines()
words = []

class Word:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        
def pos_search(*args): #находит часть речи
    pos = args[0]
    for p in pos:
        p = p.split('=')
    return p[0]

for line in text:
    jline = json.loads(line)
    if 'analysis' in jline:
        dictionary = dict()
        dictionary['word'] = jline['text']
        dictionary['num'] = len(jline['analysis'])
        if dictionary['num'] != 0:
            dictionary['freq_lemma'] = jline['analysis'][0]['lex']
            grammar = jline['analysis'][0]['gr']
            dictionary['freq_pos'] = pos_search(grammar.split(','))
        else:
            dictionary['freq_lemma'] = None
            dictionary['freq_pos'] = None
        word = Word(**dictionary)
        words.append(word)
                            
#результат
for w in words:
    print(word.word, word.num, word.freq_lemma, word.freq_pos)
