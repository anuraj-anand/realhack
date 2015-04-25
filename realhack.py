from flask import (
    Flask,
    redirect, render_template,
    request, session,
)

from data import DATA
from logic import generate_scorecard


app = Flask(__name__)

# app config
app.secret_key = 'xyz123abc098'
app.debug = True


# aliases
route = lambda _r: app.route(_r, methods=('GET', 'POST'))
render_page = lambda _p: render_template('extends/page.html', **_p)


@route('/')
def index():
    info = {
        'options': DATA.CITIES,
        'multi': False,
        'next': '/one',
        'store': 'city',
    }
    return render_page(info)


@route('/one')
def one():
    session['city'] = request.form['city']
    info = {
        'options': DATA.CUISINES,
        'multi': True,
        'next': '/two',
    }
    return render_page(info)


@route('/two')
def two():
    session['cuisines'] = tuple(request.form.keys())
    info = {
        'options': DATA.ARTS,
        'multi': True,
        'next': '/three',
    }
    return render_page(info)


@route('/three')
def three():
    session['arts'] = tuple(request.form.keys())
    info = {
        'options': DATA.SPOTS,
        'multi': True,
        'next': '/four',
    }
    return render_page(info)


@route('/four')
def four():
    session['spots'] = tuple(request.form.keys())
    user_prefs = {
        'city': session['city'],
        'cuisines': session['cuisines'],
        'arts': session['arts'],
        'spots': session['spots'],
    }
    scorecard = generate_scorecard(user_prefs)
    return scorecard


if __name__ == '__main__':
    app.run()
