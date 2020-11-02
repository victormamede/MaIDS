from .app import create_app
from .data import start_database
from .api import start_api

def build_app():
  app = create_app()

  start_database(app)
  start_api(app)

  return app