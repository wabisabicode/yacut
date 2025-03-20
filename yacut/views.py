import random
import string

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def create_full_url(path):
    base_url = request.host_url
    full_url = base_url + path
    return full_url


@app.route('/<string:short_link>')
def redirect_to_original(short_link):
    item = URLMap.get_by_short_link(short_link)
    if item is None:
        abort(404)
    return redirect(item.original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        if not original:
            flash('\"url\" является обязательным полем!')
            return render_template('index.html', form=form)

        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
            while URLMap.get_by_short_link(short) is not None:
                short = get_unique_short_id()
        elif URLMap.get_by_short_link(short) is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        elif not short.isalnum():
            flash('Указано недопустимое имя для короткой ссылки')
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()

        flash('Ваша новая ссылка готова')
        return render_template(
            'index.html',
            form=form,
            short_link=create_full_url(short)
        )
    return render_template('index.html', form=form)
