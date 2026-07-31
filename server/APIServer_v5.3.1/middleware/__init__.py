from sanic import Sanic

from middleware.base import BaseMiddleware
from middleware.response import ResponseMiddleware
from middleware.client import ClientMiddleware
from middleware.cors import CORSMiddleware

MIDDLEWARE_TUPLE: tuple[type[BaseMiddleware], ...] = (
    ClientMiddleware,
    ResponseMiddleware,
    CORSMiddleware,
)


def register_middleware(app: Sanic) -> None:
    """注册中间件"""
    for middle_cls in MIDDLEWARE_TUPLE:
        middle: BaseMiddleware = middle_cls()
        if hasattr(middle, 'before_request'):
            app.register_middleware(middle.before_request, attach_to='request')
        if hasattr(middle, 'before_response'):
            app.register_middleware(middle.before_response, attach_to='response')
    return None
