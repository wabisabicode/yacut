from flask import abort, flash, redirect, render_template, request

from . import app
from .forms import URLMapForm
from .models import URLMap


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

        url_map = URLMap.check_short_and_add(original, short)

        if not url_map:
            return render_template('index.html', form=form)

        flash('Ваша новая ссылка готова')
        return render_template(
            'index.html',
            form=form,
            short_link=create_full_url(url_map.short)
        )
    return render_template('index.html', form=form)
