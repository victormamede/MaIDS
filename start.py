import src.settings
from src.app import build_app

app = build_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
