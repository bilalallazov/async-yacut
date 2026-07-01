import random
import re
import string

from yacut.models import URLMap

DUPLICATE_MSG = 'Предложенный вариант короткой ссылки уже существует.'
RESERVED_SHORT_IDS = {'files'}
CUSTOM_ID_PATTERN = re.compile(r'^[a-zA-Z0-9]{1,16}$')
SHORT_ID_LENGTH = 6
SHORT_ID_CHARS = string.ascii_letters + string.digits


def is_valid_custom_id(custom_id):
    return bool(CUSTOM_ID_PATTERN.match(custom_id))


def get_unique_short_id(length=SHORT_ID_LENGTH):
    while True:
        short_id = ''.join(
            random.choices(SHORT_ID_CHARS, k=length)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def get_short_link(short_id):
    from flask import request
    return f'{request.host_url.rstrip("/")}/{short_id}'
