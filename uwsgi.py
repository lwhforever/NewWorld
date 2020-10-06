
from __future__ import absolute_import

import flask
import flask_cors
from flask import render_template

from config import config
import v1

from db import db


def create_app(config_name):
    config_object = config[config_name]()
    app = flask.Flask(__name__,
                      template_folder=config_object.TEMPLATE_PATH,
                      static_folder=config_object.STATIC_PATH)
    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')

    # 这里是配置数据库的相关文件
    app.config['SQLALCHEMY_DATABASE_URI'] = config_object.DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    flask_cors.CORS(app)

    # 设置一个虚拟的请求，然后来创建表
    with app.test_request_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template("index.html")

    return app


app = create_app('development')