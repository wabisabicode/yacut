from http import HTTPStatus
from flask import jsonify, request

from . import app, db
from .constants import SHORT_LINK_MAX_LEN
from .error_handlers import InvalidAPIUsage
from .models import URLMap, get_unique_short_id
from .views import create_full_url


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    custom_id = data.get('custom_id')
    # if 'custom_id' not in data or data['custom_id'] == '':
        # data['custom_id'] = get_unique_short_id()
    # if 'custom_id' not in data:
        # raise InvalidAPIUsage('BBBBBB')

    # custom_id = data['custom_id']

    # if URLMap.get_by_short_link(custom_id) is not None:
    #     raise InvalidAPIUsage(
    #         'Предложенный вариант короткой ссылки уже существует.'
    #     )
    # if not is_latin_and_num(custom_id) or len(custom_id) > SHORT_LINK_MAX_LEN:
    #     raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    try:
        url_map = URLMap.check_short_and_add(data['url'], custom_id, api=True)
    # url_map = URLMap()
    # url_map.from_dict(data)
    # db.session.add(url_map)
    # db.session.commit()

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
