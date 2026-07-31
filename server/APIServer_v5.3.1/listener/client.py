# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：client.py
@IDE     ：PyCharm 
@Author  ：
@Date    ：2024/11/10 18:42 
'''
import asyncio
from asyncio import BaseEventLoop, Task
from loguru import logger
from sanic import Sanic

from core import CurlClient
from listener.base import BaseListener


class ClientListener(BaseListener):
    """项目主监听类"""

    def __init__(self, app: Sanic):
        super().__init__(app)
        self.license_task: Task = None
        self.redis_client = None
    
    async def main_process_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        """
        项目主进程
        :param app:
        :param loop:
        :return:
        """
        pass

    async def before_server_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        """服务器启动前初始化资源"""
        pass

    async def after_server_start(self, app: Sanic, loop: BaseEventLoop) -> None:
        app.ctx.curl_client = CurlClient(app=app)
    async def before_server_stop(self, app: Sanic, loop: BaseEventLoop) -> None:
        """服务器停止前清理资源"""
        pass

