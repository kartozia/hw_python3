from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter, defaultdict
import json
import requests


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
                lem_freq = Counter(lemma)
                verb[pos] += 1
                for i in gram:
                    if i == 'несов':
                        verb['impf'] += 1                      
                    elif i == 'сов':
                        verb['perf'] += 1                
                    elif i == 'пе':
                        verb['tr'] +=1                       
                    elif i == 'нп':
                        verb['intr'] +=1 
                verb['part'] = round(((verb[pos]/words)*100),2)
    return verb, lem_freq, chart
               

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def get_info(group1, group2):
    users = []
    common = 0

    #group1: кол-во подписчиков, ID всех пользователей
    gr1 = vk_api('groups.getMembers', group_id=group1)
    members_count1 = gr1['response']['count']
    users += gr1['response']["users"]
    #закрыты ли группы?
    cl1 = vk_api('groups.getById', group_id=group1, fields ='members_count')
    for i in cl1['response']:
        if i['is_closed'] == 1:
            warn = 'Одна из групп является закрытой, поэтому мы не можем гарантировать точность полученных данных'
    cl2 = vk_api('groups.getById', group_id=group2, fields ='members_count')
    for i in cl2['response']:
        if i['is_closed'] == 1:
            warn = 'Одна из групп является закрытой, поэтому мы не можем гарантировать точность полученных данных'

    #group2: кол-во подписчиков, и проверяем через groups.isMember являются ли участники
    #первой группы участниками второй
    gr2 = vk_api('groups.getMembers', group_id=group2)
    members_count2 = gr2['response']['count']

    for start in range(0, len(users) + 1, 100):  # будем доставать информацию о 100 юзерах за один запрос
        user_info = vk_api('groups.isMember', group_id=group2, user_ids=','.join(str(i) for i in users[start:start + 100]))
        for i in user_info['response']:
            if i['member'] == 1:
                common +=1
    
    return members_count1, members_count2, common


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
        members_count1, members_count2, common, warn = get_info(group1, group2)
        return render_template('api.html', n1 = group1, n2 = group2, gr1=members_count1, gr2=members_count2, com = common)
    #можно ли сделать строку выше проще? Я пробовала с *locals(), но оно не работало :(
    return render_template('api.html')


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
