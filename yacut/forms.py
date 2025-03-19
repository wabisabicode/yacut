from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[Length(1, 256), DataRequired()]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 64), Optional()]
    )
    submit = SubmitField('Создать')