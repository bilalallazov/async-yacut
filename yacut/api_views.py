from http import HTTPStatus

from flask import Blueprint, jsonify, request

from yacut.exceptions import InvalidAPIUsage, ShortIDNotFound
from yacut.models import URLMap
from yacut.utils import get_short_link
from yacut.validators import validate_request_body

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    try:
        validate_request_body(data)
        url_map = URLMap.create(data['url'], data.get('custom_id'))
    except InvalidAPIUsage as error:
        return jsonify({'message': error.message}), error.status_code

    return jsonify(
        {'url': url_map.original, 'short_link': get_short_link(url_map.short)}
    ), HTTPStatus.CREATED


@bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    try:
        url_map = URLMap.get(short_id)
        if url_map is None:
            raise ShortIDNotFound('Указанный id не найден')
    except ShortIDNotFound as error:
        return jsonify({'message': error.message}), error.status_code
    return jsonify({'url': url_map.original}), HTTPStatus.OK
