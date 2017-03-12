import json 

mystem = open('python_mystem.json', 'r', encoding='utf-8')
text = mystem.readlines()
words = []
dictionary = {}

class Word:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        
def pos_search(*args): #находит часть речи
    pos = args[0][0]
    for p in pos:
        if '=' in p:
            p = p.split('=')
            return p[0]
        else:
            return p

for line in text:
    jline = json.loads(line)
    if 'analysis' in jline:
        dictionary['word'] = jline['text']
        dictionary['num'] = len(jline['analysis'])
        if dictionary['num'] != 0:
            dictionary['freq_lemma'] = jline['analysis'][0]['lex']
            grammar = jline['analysis'][0]['gr']
            dictionary['freq_pos'] = pos_search(grammar.split(','))
        else:
            dictionary['freq_lemma'] = 'Unknown'
            dictionary['freq_pos'] = 'Unknown'
        word = Word(**dictionary)
        words.append(word)
                            
#результат
for w in words:
    print(w.word, w.num, w.freq_lemma, w.freq_pos)
