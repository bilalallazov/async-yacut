from http import HTTPStatus

from flask import jsonify, render_template

from yacut import db


def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        if error.description.startswith('API'):
            return jsonify({'message': 'Указанный id не найден'}), (
                HTTPStatus.NOT_FOUND
            )
        return render_template('errors/404.html'), HTTPStatus.NOT_FOUND

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template(
            'errors/500.html'
        ), HTTPStatus.INTERNAL_SERVER_ERROR
