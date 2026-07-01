from flask import Blueprint, jsonify, request

from yacut import db
from yacut.models import URLMap
from yacut.utils import (
    DUPLICATE_MSG,
    RESERVED_SHORT_IDS,
    get_short_link,
    get_unique_short_id,
    is_valid_custom_id,
)

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    if not request.data:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400

    if 'url' not in data:
        return jsonify({'message': '"url" является обязательным полем!'}), 400

    url = data['url']
    custom_id = data.get('custom_id')

    if custom_id:
        if not is_valid_custom_id(custom_id):
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), 400
        if custom_id in RESERVED_SHORT_IDS:
            return jsonify({'message': DUPLICATE_MSG}), 400
        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify({'message': DUPLICATE_MSG}), 400
        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = URLMap(original=url, short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url,
        'short_link': get_short_link(short_id),
    }), 201


@bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200
