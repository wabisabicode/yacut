import random
import string

from flask import redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


@app.route('/')
def index_view():
    form = URLMapForm()
    return render_template('index.html', form=form)


@app.route('/<string:short_link>')
def redirect_to_original(short_link):
    item = URLMap.query.filter_by(short=short_link).first()
    return redirect(item.original)
