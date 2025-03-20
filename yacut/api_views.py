import re

from flask import jsonify, request

from . import app, db
from .constants import SHORT_LINK_MAX_LEN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import create_full_url, get_unique_short_id


def is_latin_and_num(s):
    return bool(re.search(r'^[a-zA-Z0-9]+$', s))


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' not in data or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()

    custom_id = data['custom_id']

    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if not is_latin_and_num(custom_id) or len(custom_id) > SHORT_LINK_MAX_LEN:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()

    return_dict = dict(
        url=url_map.original,
        short_link=create_full_url(url_map.short)
    )
    return jsonify(return_dict), 201


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    item = URLMap.query.filter_by(short=short_id).first()
    print(item, type(item))
    if item is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': item.original}), 200