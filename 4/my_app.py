from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

ask = {
   'var'   : ['Собаки', 'Кошки']
}

@app.route('/')
def index():
    urls = {'Опрос': url_for('index'),
            'Результаты опроса': url_for('result'),}
    if request.args:
        name = request.args['name']
        animal = request.args['animal']
        return render_template('results.html', name=name, animal=animal)
    return render_template('index.html', urls=urls, data=ask)


@app.route('/results')
def result():
    votes = {}
    votes['Собаки'] = 0
    votes['Кошки'] = 0
    if request.args['animal'] == 'dog':
        votes['Собаки'] += 1
        return render_template('results.html', name=request.args['name'], votes=votes)
    if request.args['animal'] == 'cat':
        votes['Кошки'] += 1
        return render_template('results.html', name=request.args['name'], votes=votes)
    

if __name__ == '__main__':
    app.run(debug=True)
