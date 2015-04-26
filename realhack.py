from flask import (
    Flask,
    redirect, render_template,
    request, session,
)

from data import DATA
from logic import Scorecard


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
        'heading': 'City',
    }
    return render_page(info)


@route('/one')
def one():
    session['city'] = request.form['city']
    info = {
        'options': DATA.CUISINES,
        'multi': True,
        'next': '/two',
        'heading': 'Cuisines'
    }
    return render_page(info)


@route('/two')
def two():
    session['cuisines'] = tuple(request.form.keys())
    info = {
        'options': DATA.ARTS,
        'multi': True,
        'next': '/three',
        'heading': 'Arts',
    }
    return render_page(info)


@route('/three')
def three():
    session['arts'] = tuple(request.form.keys())
    info = {
        'options': DATA.SPOTS,
        'multi': True,
        'next': '/four',
        'heading': 'Spots',
    }
    return render_page(info)


@route('/four')
def four():
    spots = tuple(request.form.keys())
    session['spots'] = spots

    city = session['city']
    localities = DATA.LOCALITIES[city]
    cuisines = session['cuisines']
    arts = session['arts']

    user_prefs = {
        'city': city,
        'localities': localities,
        'cuisines': cuisines,
        'arts': arts,
        'spots': spots,
    }
    scorecard = Scorecard.generate(user_prefs)
    winner, ratings, distances = Scorecard.select_winner(scorecard)

    info = {
        'winner': winner,
        'ratings': ratings,
        'distances': distances,
    }

    return render_template('extends/final.html', **info)


if __name__ == '__main__':
    app.run()
