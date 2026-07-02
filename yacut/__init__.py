import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from yacut.constants import SHORT_ID_GENERATION_ATTEMPTS

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DISK_TOKEN'] = os.getenv('DISK_TOKEN')
    app.config['SHORT_ID_GENERATION_ATTEMPTS'] = int(
        os.getenv(
            'SHORT_ID_GENERATION_ATTEMPTS',
            SHORT_ID_GENERATION_ATTEMPTS
        )
    )

    db.init_app(app)

    from yacut import api_views, error_handlers, views
    app.register_blueprint(views.bp)
    app.register_blueprint(api_views.bp)
    error_handlers.register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
