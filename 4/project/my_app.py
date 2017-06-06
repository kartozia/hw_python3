from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter, defaultdict, OrderedDict
import json
import requests
from nltk.stem.snowball import SnowballStemmer
import itertools


m = Mystem()
app = Flask(__name__)


def verb_analisys(text):
    gram = []
    lemma = []
    ana = m.analyze(text)
    verb = defaultdict(int)
    chart = defaultdict(int)
    words = len(text.split())
    for i in ana:     
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            pos = i['analysis'][0]['gr'].split('=')[0].split(',')[0]
            chart[pos] += 1
            gram1 = i['analysis'][0]['gr'].split('=')[0].split(',')
            gram2 = i['analysis'][0]['gr'].split('=')[1].split(',')
            gram = gram1 + gram2
            if pos == 'V':
                lex = i['analysis'][0]['lex']
                lemma.append(lex)
                lem_freq = OrderedDict(sorted(Counter(lemma).items(), key=lambda t: t[1], reverse=True))
##                for i in freq:
##                    lem_freq.append(i)
                verb['кол-во глаголов в тексте'] += 1
                for i in gram:
                    if i == 'несов':
                        verb['несовершенного вида'] += 1                      
                    elif i == 'сов':
                        verb['совершенного вида'] += 1                
                    elif i == 'пе':
                        verb['переходных'] +=1                       
                    elif i == 'нп':
                        verb['непереходных'] +=1 
                verb['доля глаголов в тексте'] = round(((verb['кол-во глаголов в тексте']/words)*100),2)
    return verb, lem_freq, chart
               

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def get_info(group1, group2):
    #group1: кол-во подписчиков, ID всех пользователей
    gr1 = vk_api('groups.getMembers', group_id=group1)
    members_count1 = gr1['response']['count']
    users = {i for i in gr1['response']["users"]}
    #закрыты ли группы?
    cl1 = vk_api('groups.getById', group_id=group1)
    name1 = cl1['response'][0]["name"]
    for i in cl1['response']:
        if i['is_closed'] == 1:
            warn = 'Одна из групп является закрытой, поэтому мы не можем гарантировать точность полученных данных'
        else:
            warn = ''
    cl2 = vk_api('groups.getById', group_id=group2)
    name2 = cl2['response'][0]["name"]
    for i in cl2['response']:
        if i['is_closed'] == 1:
            warn = 'Одна из групп является закрытой, поэтому мы не можем гарантировать точность полученных данных'
        else:
            warn = ''

    #group2: кол-во подписчиков, и проверяем через groups.isMember являются ли участники
    #первой группы участниками второй
    gr2 = vk_api('groups.getMembers', group_id=group2)
    members_count2 = gr2['response']['count']
    users2 = {i for i in gr2['response']["users"]}

    count = itertools.filterfalse(lambda x: x not in users2, users)
    common = sum(1 for i in count)
    
    return members_count1, members_count2, common, warn, name1, name2

def exact_search(word):
    sentence = []
    file = open('/home/kartozia/mysite/corpus.txt', 'r', encoding="utf-8")
    corpus = file.readlines()
    if len(word) > 0:
        for line in corpus:
            sent = line.split()
            for s in sent:
                if word == s.strip('!?:;.,'):
                    sentence.append(line)
        if len(sentence) < 1:
            sentence.append('По вашему запросу ничего не найдено')
    else:
        pass
    file.close()
    return sentence

def search(word):
    sentence = []
    stemmer = SnowballStemmer("russian")
    file = open('/home/kartozia/mysite/corpus.txt', 'r', encoding="utf-8")
    corpus = file.readlines()
    if len(word) > 0:
        word_stem = stemmer.stem(word)
        for line in corpus:
            if word_stem in line:
                sentence.append(line)
        if len(sentence) < 1:
            sentence.append('По вашему запросу ничего не найдено')
    else:
        pass
    file.close()
    return sentence

def collocation_search(word):
    bigram = []
    stemmer = SnowballStemmer("russian")
    file = open('/home/kartozia/mysite/collocations.txt', 'r', encoding="utf-8")
    corpus = file.readlines()
    if len(word) > 0:
        word_stem = stemmer.stem(word)
        for line in corpus:
            if word_stem in line:
                bigram.append(line)
        if len(bigram) < 1:
            bigram.append('По вашему запросу ничего не найдено')
    else:
        pass
    file.close()
    return bigram
    

@app.route('/pos', methods=['get', 'post'])
def pos_text():
    if request.form:
        text = request.form['text']
        verb, lem_freq, chart = verb_analisys(text)
        return render_template('mystem.html', input=text, data=verb, lemma=lem_freq, gchart = chart)
    return render_template('mystem.html', data={}, gchart = {})

@app.route('/vk', methods=['get', 'post'])
def vk():
    if request.form:
        group1 = request.form['group1']
        group2 = request.form['group2']
        members_count1, members_count2, common, warn, name1, name2 = get_info(group1, group2)
        return render_template('api.html', **locals())
 #      return render_template('api.html', n1 = group1, n2 = group2, gr1=members_count1, gr2=members_count2, com = common)
    #можно ли сделать строку выше проще? Я пробовала с *locals(), но оно не работало :(
    return render_template('api.html')

@app.route('/nltk', methods=['get', 'post'])
def corpus():
    if request.form:
        all_forms = request.form['all']
        exact = request.form['exact']
        collocation = request.form['collocation']
        af = search(all_forms)
        ex = exact_search(exact)
        clctn = collocation_search(collocation)
        return render_template('nltk.html', **locals())
    return render_template('nltk.html')



@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
