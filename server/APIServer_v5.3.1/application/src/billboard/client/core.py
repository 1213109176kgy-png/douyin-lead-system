# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager
@File    ：client.py
@IDE     ：PyCharm
@Author  ：
@Date    ：2024/11/14 21:32
'''
import json
import random

from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.billboard.client.parameter import DOUYIN_BILLBOARD_HEADER, URL_PATH
from core import json_success_response, get_device_data, CustomException
from libs import get_request_data, get_request_proxy


class BaseView(HTTPMethodView):
    URL_MAPPING = URL_PATH

    async def _headers(self,  request):
        cookie = await self.get_random_data(request)
        headers = DOUYIN_BILLBOARD_HEADER.copy()
        headers['Cookie'] = cookie
        return headers

    async def fetch_data(self, request, endpoint, params=None, json_data=None, proxy=None):
        url = request.app.ctx.BASE_BILLBOARD + endpoint
        try:
            if json_data:
                response = await request.app.ctx.curl_client.http_post(url, json=json_data, headers=await self._headers(request), proxy=proxy)
            else:
                response = await request.app.ctx.curl_client.http_get(url, params=params, headers=await self._headers(request),  proxy=proxy)
            data = json.loads(response.text)
            return json_success_response(data)
        except Exception as e:
            raise e

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        proxy = await get_request_proxy(request)
        data['proxy'] = proxy
        return await self.process_request(request, data)

    async def get_random_data(self, request):
        acc = await get_device_data(request.app, "billboard")
        return acc

    async def process_request(self, request: Request, data) -> HTTPResponse:
        raise Exception("没有模板")