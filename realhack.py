from flask import (
    Flask, render_template,
)

from data import DATA


app = Flask(__name__)


@app.route('/')
def index():
    info = {
        'cities': DATA.CITIES,
    }
    return render_template('index.html', **info)


if __name__ == '__main__':
    app.run(debug=True)
