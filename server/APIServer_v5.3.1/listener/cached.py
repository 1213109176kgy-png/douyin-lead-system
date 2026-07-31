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
from asyncio import BaseEventLoop
from loguru import logger
from sanic import Sanic
from libs.cached import RedisClient
from listener.base import BaseListener


class CachedListener(BaseListener):
    """项目缓存监听类"""

    def __init__(self, app: Sanic):
        super().__init__(app)
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
        try:
            if app.config.CHINESE_PROXY_URL and app.config.CHINESE_PROXY_URL == "redis":
                redis_client = RedisClient(redis_url=app.config.REDIS_URL)
                await redis_client.init()
                if not await redis_client.check_connection():
                    raise RuntimeError("Redis 链接失败")
                else:
                    app.ctx.redis_client = redis_client
                    logger.info("Redis IP池链接成功")
        except Exception as e:
            logger.warning(f"Redis IP池链接失败 {e}")

    async def before_server_stop(self, app: Sanic, loop: BaseEventLoop) -> None:
        pass