from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import create_full_url, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id()
    if not data['custom_id'].isalnum():
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if len(data['custom_id']) > 16:
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