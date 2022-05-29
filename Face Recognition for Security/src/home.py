from flask import render_template

from flask import current_app

from . import app


@app.route('/')
def welcome():
    return render_template('Index.html')
