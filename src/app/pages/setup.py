def start_pages(app):
    @app.route('/')
    def index():
        return 'MaIDS App'