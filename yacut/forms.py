from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import ORIGINAL_LINK_MAX_LEN, SHORT_LINK_MAX_LEN


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[Length(1, ORIGINAL_LINK_MAX_LEN), DataRequired()]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, SHORT_LINK_MAX_LEN), Optional()]
    )
    submit = SubmitField('Создать')