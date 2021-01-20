from flask import render_template
from ..data.tables.equipment import Equipment


def start_pages(app):
    @app.route('/')
    def index():
        results = Equipment.query.all()

        equips = [equipment.as_dict() for equipment in results]

        return render_template('index.html', equipment=equips)
