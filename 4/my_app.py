from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

ask = {
   'var'   : ['Собаки', 'Кошки']
}
name = 'result.txt'

@app.route('/')
def index():
    urls = {'Опрос': url_for('index'),
            'Результаты опроса': url_for('result'),}
    if request.args:
        name = request.args['name']
        vote = request.args.get('var')
        res = open(name, 'a', encoding='utf-8')
        res.write(vote + '\n' )
        res.close() 
        return render_template('results.html', name=name)
    return render_template('index.html', urls=urls, data=ask)


@app.route('/results')
def result():
    votes = {}
    file  = open(name, 'r')
    for a in ask['var']:
        votes[a] = 0
    for line in file:
        vote = line.rstrip("\n")
        votes[vote] += 1 
    return render_template('results.html', data=ask, votes=votes)   

if __name__ == '__main__':
    app.run(debug=True)
