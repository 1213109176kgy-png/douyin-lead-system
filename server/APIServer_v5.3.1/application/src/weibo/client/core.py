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
@File    ：core.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 13:44 
@WebSite ：
'''
import json
import random
import re
from urllib.parse import urlparse

import httpx
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from core import get_device_data
from libs.request import get_request_data, get_request_proxy

DEFAULT_HEADERS = {
    "Referer": "https://weibo.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55"
}
MOBILE_HEADERS = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36 Edg/142.0.0.0",
  "Connection": "keep-alive",
  "Accept": "application/json, text/plain, */*",
  "Accept-Encoding": "gzip, deflate, br",
  "accept-language": "zh-CN,zh;q=0.9",
  "cache-control": "no-cache",
  "mweibo-pwa": "1",
  "pragma": "no-cache",
  "priority": "u=1, i",
  "referer": "https://m.weibo.cn/",
  "sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
  "sec-ch-ua-mobile": "?1",
  "sec-ch-ua-platform": "\"Android\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "x-requested-with": "XMLHttpRequest"
}

URLS = {
    "USER_DATA": "https://m.weibo.cn/api/container/getIndex",
    "USER_POST": "https://m.weibo.cn/api/container/getIndex",
    "POST_DETAIL": "https://weibo.com/ajax/statuses/show",
    "POST_LONG_DETAIL": "https://weibo.com/ajax/statuses/longtext",
    "POST_COMMENT": "https://weibo.com/ajax/statuses/buildComments",
    "TOPIC_DETAIL": "https://m.weibo.cn/api/container/getIndex",
    "TOPIC_DETAIL_URL": "https://m.s.weibo.com/ajax_topic/detail",
    "TOPIC_TREND_URL": "https://m.s.weibo.com/ajax_topic/trend",
    "USER_VIDEO_POST": "https://weibo.com/ajax/profile/getWaterFallContent",
    "SEARCH_URL": "https://m.weibo.cn/api/container/getIndex",
    "SHORT_VIDEO_URL": "https://h5.video.weibo.com/api/component?page=/tv/show/",
}


class RequestHandler:
    @staticmethod
    async def fetch_data(request: Request, url: str, params: dict, data: dict = None, headers: dict = None) -> dict:
        proxy = await get_request_proxy(request)
        try:
            if not data:
                response = await request.app.ctx.curl_client.http_get(url=url, params=params, headers=headers,
                                                                      proxy=proxy)
            else:
                response = await request.app.ctx.curl_client.http_post(url=url, data=data, headers=headers, proxy=proxy)
            if response.status_code == 200 and response.text:
                return json.loads(response.text)
        except Exception as e:
            raise e

    @staticmethod
    async def request_data(request: Request, url: str, params: dict, data: dict = None, cookie: str = None,
                           headers: dict = None) -> dict:
        headers = DEFAULT_HEADERS.copy() if not headers else headers
        if cookie:
            headers['Cookie'] = cookie
        return await RequestHandler.fetch_data(request, url, params, data, headers)

    @staticmethod
    async def get_request_data(request: Request) -> dict:
        return await get_request_data(request)

    @staticmethod
    async def get_user_id(share_text: str) -> str:
        match = re.search(r"/u/(\d+)", share_text)
        return match.group(1) if match else ""

    @staticmethod
    async def get_post_id(share_text: str) -> str:
        parsed_url = urlparse(share_text)
        path = parsed_url.path
        match = re.search(r'/(\d+)$', path) or re.search(r'/([^/]+)$', path)
        return match.group(1) if match else ""

    @staticmethod
    async def get_sub(request: Request) -> str:
        acc = await get_device_data(request.app, "weibo")
        return acc

    @staticmethod
    async def get_cookie(request: Request) -> str:
        data = {
            "cb": "visitor_gray_callback",
            "ver": "20250916",
            "request_id": "",
            "tid": "01AdWJwiPhpZdO70yJd0Bp72RDuRDfi4IMU_DBeI7Emk4G",
            "from": "weibo",
            "webdriver": "false",
            "rid": "",
            "return_url": "https://m.weibo.cn/u/1699432410?",
            "jumpfrom": "weibocom"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36 Edg/142.0.0.0",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua-platform": "\"Android\"",
            "if-modified-since": "0",
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "origin": "https://visitor.passport.weibo.cn",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://visitor.passport.weibo.cn/",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "tid=01AdWJwiPhpZdO70yJd0Bp72RDuRDfi4IMU_DBeI7Emk4G",
            "priority": "u=1, i"
        }
        proxy = await get_request_proxy(request)
        response = await request.app.ctx.curl_client.http_post(url="https://visitor.passport.weibo.cn/visitor/genvisitor2", data=data, headers=headers, proxy=proxy)
        cookie = "; ".join([f"{key}={value}" for key, value in response.cookies.items()])
        return cookie


class BaseView(HTTPMethodView):
    async def post(self, request: Request) -> HTTPResponse:
        data = await RequestHandler.get_request_data(request)
        return await self.handle_request(request, data)

    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        raise Exception("没有模版")
