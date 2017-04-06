import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    urls = {'Опрос': url_for('index'),
            'Результаты опроса': url_for('result')
            }
    return render_template('index.html', urls=urls)


@app.route('/results')
def result():
    dogs = 0
    cats = 0
    if request.args['animal'] == 'Собаки':
        dogs += 1
    if request.args['animal'] == 'Кошки':
        animal = request.args['animal']
    return render_template('results.html', name=request.args['name'], dogs=dogs, cats=cats)

if __name__ == '__main__':
    app.run(debug=True)
