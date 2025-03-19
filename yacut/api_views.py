from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if 'original' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({url_map.to_dict()}), 201