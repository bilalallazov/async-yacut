import random
import string

from flask import current_app, url_for

from yacut.constants import DUPLICATE_MESSAGE, SHORT_ID_DEFAULT_LENGTH
from yacut.exceptions import InvalidAPIUsage

SHORT_ID_CHARS = string.ascii_letters + string.digits


def get_unique_short_id(getter, length=SHORT_ID_DEFAULT_LENGTH):
    max_attempts = current_app.config['SHORT_ID_GENERATION_ATTEMPTS']
    for _ in range(max_attempts):
        short_id = ''.join(random.choices(SHORT_ID_CHARS, k=length))
        if getter(short_id) is None:
            return short_id
    raise InvalidAPIUsage(DUPLICATE_MESSAGE)


def get_short_link(short_id):
    return url_for('views.redirect_view', short_id=short_id, _external=True)
