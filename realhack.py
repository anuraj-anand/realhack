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
    info = {
        'options': DATA.CITIES,
        'multi': False,
        'next': '/one',
        'store': 'city',
    }
    return render_template('page.html', **info)


@route('/one')
def one():
    session['city'] = request.form['city']
    info = {
        'options': DATA.CUISINES,
        'multi': True,
        'next': '/two',
    }
    return render_template('page.html', **info)


@route('/two')
def two():
    session['cuisines'] = tuple(request.form.keys())
    info = {
        'options': DATA.ARTS,
        'multi': True,
        'next': '/three',
    }
    return render_template('page.html', **info)


@route('/three')
def three():
    session['arts'] = tuple(request.form.keys())
    info = {
        'options': DATA.SPOTS,
        'multi': True,
        'next': '/four',
    }
    return render_template('page.html', **info)


@route('/four')
def four():
    session['spots'] = tuple(request.form.keys())
    print(str(session))
    return redirect('/')


if __name__ == '__main__':
    app.run()
