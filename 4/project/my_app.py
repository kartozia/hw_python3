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
    words = len(text.split())
    for i in ana:     
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            pos = i['analysis'][0]['gr'].split('=')[0].split(',')[0]
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
    return verb, lem_freq


                
                

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def get_info(group):
    users = []

    result = vk_api('groups.getMembers', group_id=group)
    members_count = result['response']['count']
    users += result['response']["users"]

    while len(users) < members_count:
        result = vk_api('groups.getMembers', group_id=group, offset=len(users))
        users += result['response']["users"]

    cities = []
    for start in range(0, len(users) + 1, 100):  # будем доставать информацию о 100 юзерах за один запрос
        user_info = vk_api('users.get', user_ids=','.join(str(i) for i in users[start:start + 100]), fields='city',
                           v='5.63')
        cities += [(c["city"]['id'], c["city"]['title']) for c in user_info['response']
                   if 'city' in c]  # эта проверка нужна, чтобы отфильтровать пользователей, удаливших страницу
    city_dict = Counter([i[1] for i in cities]).most_common()
    return city_dict


@app.route('/pos', methods=['get', 'post'])
def pos_text():
    if request.form:
        text = request.form['text']
        verb, lem_freq = verb_analisys(text)
        return render_template('mystem.html', input=text, data=verb, lemma=lem_freq)
    return render_template('mystem.html', data={})
@app.route('/vk', methods=['get', 'post'])


def vk():
    if request.form:
        group_id = request.form['group_id']
        info = get_info(group_id)
        return render_template('api.html', **locals())
    return render_template('api.html')


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
