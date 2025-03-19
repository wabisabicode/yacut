from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>')
def get_original_link(short_id):
    item = URLMap.query.filter_by(short=short_id).first()
    if item is None:
        raise InvalidAPIUsage('Указанный id не найден')
    return jsonify({'url': item.original}), 200