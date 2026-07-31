from sanic import Sanic

from listener.base import BaseListener
from listener.cached import CachedListener
from listener.client import ClientListener
from listener.docs import DocsListener
from listener.main_process import MainProcessListener

LISTENER_TUPLE: tuple[type[BaseListener], ...] = (
DocsListener,
    ClientListener,
    MainProcessListener,
    CachedListener,

)


def register_listener(app: Sanic) -> None:
    """注册监听"""
    for listener_cls in LISTENER_TUPLE:
        listener: BaseListener = listener_cls(app=app)
        for event in ('main_process_start', 'before_server_start', 'after_server_start', 'before_server_stop', 'after_server_stop'):
            if hasattr(listener, event):
                app.register_listener(getattr(listener, event), event)
    return None
