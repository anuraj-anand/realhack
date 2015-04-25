from flask import (
    Flask, render_template,
    request, session,
)

from data import DATA


app = Flask(__name__)

# app config
app.secret_key = 'xyz123abc098'
app.debug = True


@app.route('/')
def index():
    info = {'cities': DATA.CITIES}
    return render_template('index.html', **info)


@app.route('/one')
def one():
    session['city'] = request.form['city']
    info = {'cuisines': DATA.CUISINES}
    return render_template('one.html', **info)


@app.route('/two')
def two():
    session['cuisines'] = tuple(request.form.keys())
    info = {'arts': DATA.ARTS}
    return render_template('two.html', **info)


@app.route('/three')
def three():
    session['arts'] = tuple(request.form.keys())
    info = {'spots': DATA.SPOTS}
    return render_template('three.html', **info)


if __name__ == '__main__':
    app.run()
