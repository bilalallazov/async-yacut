from datetime import datetime

from yacut import db
from yacut.constants import (
    DUPLICATE_MESSAGE,
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_ID_MAX_LENGTH,
)
from yacut.exceptions import InvalidAPIUsage
from yacut.utils import get_unique_short_id
from yacut.validators import validate_custom_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def create(original, custom_id=None):
        validate_custom_id(custom_id)
        if custom_id and URLMap.get(custom_id):
            raise InvalidAPIUsage(DUPLICATE_MESSAGE)
        short_id = custom_id or get_unique_short_id(URLMap.get)
        url_map = URLMap(original=original, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map
