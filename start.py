import os
import src.settings
from src.app import build_app
from flask import Flask

app = Flask(__name__, static_url_path="/static", static_folder="res")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE") or "sqlite:///:memory:"
app.config["SQLALCHEMY_ECHO"] = os.getenv("SQL_LOGS") == "TRUE"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

build_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
