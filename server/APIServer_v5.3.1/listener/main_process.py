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
from core.permit.licenses import License
from listener.base import BaseListener


class MainProcessListener(BaseListener):
    """项目进程类"""

    def __init__(self, app: Sanic):
        super().__init__(app)
        self.license_task: Task = None

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
        application_status = License(app=app)
        await application_status.main_process_licenses()
        self.license_task = asyncio.create_task(application_status.main_process_task())
        app.ctx.tiktok_device_ttwid = []
        logger.info("MoreAPI进程启动成功")

    async def before_server_stop(self, app: Sanic, loop: BaseEventLoop) -> None:
        if hasattr(self, 'license_task') and self.license_task is not None and not self.license_task.done():
            logger.info("正在清理MoreAPI进程...")
            self.license_task.cancel()
            try:
                await self.license_task
            except asyncio.CancelledError:
                logger.info("MoreAPI进程已取消")
            except Exception as e:
                logger.error(f"取消MoreAPI进程时出错: {e}")


