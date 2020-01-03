from App.views import blue,init_blue
from App.views1 import blue as blue1,init_blue1
from App.views2 import blue as blue2,init_blue2
from App.settings import config
from App.ext import init_ext
from flask import Flask


def create_app(env_name=None):
    app = Flask(__name__)

    app.config.from_object(config.get("develop"))#开发环境

    init_ext(app)

    init_blue(app)

    init_blue1(app)

    init_blue2(app)

    return app
