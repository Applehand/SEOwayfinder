from flask import Flask
from web.routes import init_routes
from spider.storage import create_tables
create_tables()


def create_app():
    app = Flask(__name__)

    init_routes(app)

    return app
