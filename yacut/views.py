from flask import redirect, render_template

from . import app, db
from .models import URLMap


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/<string:short_link>')
def redirect_to_original(short_link):
    item = URLMap.query.filter_by(short=short_link).first()
    return redirect(item.original)
