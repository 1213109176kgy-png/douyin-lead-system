#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：docs.py
@IDE     ：PyCharm 

@Date    ：2025/5/15 14:50 
'''
from asyncio import BaseEventLoop
from sanic import Sanic

from listener import BaseListener
from core.permit.openapi import register_swagger_routes



class DocsListener(BaseListener):
    """API监听器"""

    async def main_process_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        """
        项目主进程
        :param app:
        :param loop:
        :return:
        """
        pass

    async def before_server_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        await register_swagger_routes(app)

    async def after_server_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        """服务器启动后"""
        pass

    async def before_server_stop(self, app: Sanic, loop: BaseEventLoop) -> None:
        pass