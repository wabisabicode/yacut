from datetime import datetime

from yacut import db

from .constants import ORIGINAL_LINK_MAX_LEN, SHORT_LINK_MAX_LEN


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LEN), nullable=False)
    short = db.Column(db.String(SHORT_LINK_MAX_LEN), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    @staticmethod
    def get_by_short_link(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    def from_dict(self, data):
        field_mapping = {
            'url': 'original',
            'custom_id': 'short'
        }

        for api_field, model_field in field_mapping.items():
            if api_field in data:
                setattr(self, model_field, data[api_field])
