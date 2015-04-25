from flask import (
    Flask, render_template,
    request, session,
)

from data import DATA


app = Flask(__name__)


@app.route('/')
def index():
    info = {'cities': DATA.CITIES}
    return render_template('index.html', **info)


@app.route('/one')
def one():
    session['city'] = request.form['city']
    info = {'cuisines': DATA.CUISINES}
    return render_template('one.html', **info)


if __name__ == '__main__':
    app.run(debug=True)
