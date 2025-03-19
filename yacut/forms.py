from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(validators=[Length(1, 256), DataRequired()])
    custom_id = URLField(validators=[Length(1, 64), Optional()])
    submit = SubmitField()