import re

from yacut.constants import (
    DUPLICATE_MESSAGE,
    EMPTY_BODY_MESSAGE,
    INVALID_NAME_MESSAGE,
    MISSING_URL_MESSAGE,
    RESERVED_SHORT_IDS,
    SHORT_ID_MAX_LENGTH,
)
from yacut.exceptions import InvalidAPIUsage

CUSTOM_ID_PATTERN = re.compile(
    rf'^[a-zA-Z0-9]{{1,{SHORT_ID_MAX_LENGTH}}}$'
)


def validate_request_body(data):
    if data is None:
        raise InvalidAPIUsage(EMPTY_BODY_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(MISSING_URL_MESSAGE)


def validate_custom_id(custom_id):
    if not custom_id:
        return
    if not CUSTOM_ID_PATTERN.fullmatch(custom_id):
        raise InvalidAPIUsage(INVALID_NAME_MESSAGE)
    if custom_id in RESERVED_SHORT_IDS:
        raise InvalidAPIUsage(DUPLICATE_MESSAGE)
    from yacut.models import URLMap

    if URLMap.get(custom_id) is not None:
        raise InvalidAPIUsage(DUPLICATE_MESSAGE)
