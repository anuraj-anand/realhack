from flask import (
    Flask,
    redirect, render_template,
    request, session,
)

from data import DATA


app = Flask(__name__)

# app config
app.secret_key = 'xyz123abc098'
app.debug = True


# aliases
route = lambda _r: app.route(_r, methods=('GET', 'POST'))


@route('/')
def index():
    info = {'cities': DATA.CITIES}
    return render_template('index.html', **info)


@route('/one')
def one():
    session['city'] = request.form['city']
    info = {'cuisines': DATA.CUISINES}
    return render_template('one.html', **info)


@route('/two')
def two():
    session['cuisines'] = tuple(request.form.keys())
    info = {'arts': DATA.ARTS}
    return render_template('two.html', **info)


@route('/three')
def three():
    session['arts'] = tuple(request.form.keys())
    info = {'spots': DATA.SPOTS}
    return render_template('three.html', **info)


@route('/four')
def four():
    session['spots'] = tuple(request.form.keys())
    print(str(session))
    return redirect('/')


if __name__ == '__main__':
    app.run()
