import random
import re
import string
from datetime import datetime

from flask import flash

from yacut import db

from .constants import ORIGINAL_LINK_MAX_LEN, SHORT_LINK_MAX_LEN
from .error_handlers import InvalidAPIUsage


def is_latin_and_num(s):
    return bool(re.search(r'^[a-zA-Z0-9]+$', s))


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_LINK_MAX_LEN), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    @staticmethod
    def get_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_or_create_short(original, short, api=False):
        if not short or short == '':
            short = get_unique_short_id()
            while URLMap.get_by_short_link(short) is not None:
                short = get_unique_short_id()

        elif URLMap.get_by_short_link(short) is not None:
            msg = 'Предложенный вариант короткой ссылки уже существует.'
            if api:
                raise InvalidAPIUsage(msg)
            else:
                flash(msg)
                return None

        if not is_latin_and_num(short) or len(short) > SHORT_LINK_MAX_LEN:
            msg = 'Указано недопустимое имя для короткой ссылки'
            if api:
                raise InvalidAPIUsage(msg)
            else:
                flash(msg)
                return None

        url_map = URLMap(
            original=original,
            short=short
        )

        db.session.add(url_map)
        db.session.commit()
        return url_map
