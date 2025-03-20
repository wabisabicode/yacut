from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import create_full_url


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    custom_id = data.get('custom_id')

    try:
        url_map = URLMap.check_short_and_add(data['url'], custom_id, api=True)

        return_dict = dict(
            url=url_map.original,
            short_link=create_full_url(url_map.short)
        )
        return jsonify(return_dict), HTTPStatus.CREATED
    except InvalidAPIUsage as e:
        raise e


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    item = URLMap.get_by_short_link(short_id)
    if item is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': item.original}), HTTPStatus.OK
