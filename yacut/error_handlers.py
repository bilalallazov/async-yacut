from flask import jsonify, render_template


def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        if error.description.startswith('API'):
            return jsonify({'message': 'Указанный id не найден'}), 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
