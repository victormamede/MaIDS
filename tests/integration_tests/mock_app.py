import os
from flask import Flask


def create_mock_app():
    app = Flask(__name__, static_url_path='/static', static_folder='res')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE') or 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = os.getenv('SQL_LOGS') == 'TRUE'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app