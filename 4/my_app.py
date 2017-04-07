from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    urls = {'Опрос': url_for('index'),
            'Результаты опроса': url_for('result'),}
    if request.args:
        name = request.args['name']
        animal = request.args['animal']
        return render_template('results.html', urls=urls, name=name, animal=animal)
    return render_template('index.html')


@app.route('/results')
def result():
    votes = {}
    if request.args['animal'] == 'Собаки':
        votes['Собаки'] += 1
    if request.args['animal'] == 'Кошки':
        votes['Кошки'] += 1
    return render_template('results.html', name=request.args['name'], votes=votes)

if __name__ == '__main__':
    app.run(debug=True)
