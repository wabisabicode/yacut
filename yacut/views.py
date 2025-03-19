import random
import string

from flask import flash, redirect, render_template, request, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


@app.route('/<string:short_link>')
def redirect_to_original(short_link):
    item = URLMap.query.filter_by(short=short_link).first()
    return redirect(item.original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        # if not original:
        #      raise FormError('\"url\" является обязательным полем!')

        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
            while URLMap.query.filter_by(short=short).first() is not None:
                short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()

        flash('Ваша новая ссылка готова')
        base_url = request.host_url
        short_link = base_url + short
        return render_template('index.html', form=form, short_link=short_link)
    return render_template('index.html', form=form)
