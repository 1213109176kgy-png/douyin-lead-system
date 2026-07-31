#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：base.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 9:47 
'''
import http.cookies
import json
import re

from bilibili_api import search
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.bilibili.client.parameter import BASE_PC_HEADERS, search_type_map, order_type_map
from core import json_success_response
from libs import get_request_data, get_request_proxy


class BaseView(HTTPMethodView):

    async def _headers(self, request):
        headers = BASE_PC_HEADERS.copy()
        return headers

    async def fetch_data(self, request, url, params=None, json_data=None, headers=None):
        proxy = await get_request_proxy(request)
        try:
            if json_data:
                response = await request.app.ctx.curl_client.http_post(url, json=json_data, headers=await self._headers(
                    request) if not headers else headers, proxy=proxy)
            else:
                response = await request.app.ctx.curl_client.http_get(url, params=params, headers=await self._headers(
                    request) if not headers else headers, proxy=proxy)
            return response
        except Exception as e:
            raise e

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        proxy = await get_request_proxy(request)
        data['proxy'] = proxy
        return await self.process_request(request, data)

    async def parse_script(self, response, pattern):
        try:
            script_list = re.findall(pattern, response.text)
            if not script_list:
                return None
            return json.loads(script_list[0])
        except Exception:
            return None

    async def process_request(self, request: Request, data) -> HTTPResponse:
        raise Exception("没有模板")

    def get_search_type_and_order(self, search_type, order_type):

        search_type_obj = search_type_map.get(search_type, search.SearchObjectType.PHOTO)

        if search_type in order_type_map:
            order_mapping = order_type_map[search_type]
            order_type_obj = order_mapping.get(order_type, order_mapping["DEFAULT"])
        else:
            order_type_obj = order_type

        return search_type_obj, order_type_obj

    def parse_cookie(self, cookie):
        if cookie:
            cookie = http.cookies.SimpleCookie(cookie)
            return {key: morsel.value for key, morsel in cookie.items()}
        return {}

    def check_cookie(self, cookie_dict):
        return all(key in cookie_dict for key in ['buvid3', 'SESSDATA', 'bili_jct'])

    async def get_buvid3(self, request, proxy):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        response = await request.app.ctx.curl_client.http_get("https://www.bilibili.com/",
                                                            headers=headers,
                                                            proxy=proxy)

        cookie = '; '.join([f'{k}={v}' for k, v in response.cookies.items()])
        return cookie
