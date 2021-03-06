from .data import start_database
from .api import start_api
from .pages import start_pages


def build_app(app):
    start_database(app)
    start_api(app)
    start_pages(app)

    return app
