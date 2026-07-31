from sanic import Sanic
from sanic_ext import Extend

from application.config import BaseConfig
from application.src import register_blueprint
from core import setup_exception_handlers
from listener import register_listener
from middleware import register_middleware


def create_app():
    """
    创建项目app
    :return:
    """
    app: Sanic = Sanic(__name__)
    app.update_config(BaseConfig)
    # 注册监听
    register_listener(app)
    # 注册中间件
    register_middleware(app)
    # 注册异常
    setup_exception_handlers(app)
    # 注册路由
    register_blueprint(app)

    # 初始化 Sanic Extensions
    Extend(app)

    return app