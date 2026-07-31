#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 21:11 
'''
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.lemon.client.core import BaseLemon
from libs.request import get_request_data


class AwemeDetailView(HTTPMethodView):
    """
    获取单一作品详情
    """

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        lemon = BaseLemon(request)
        return await lemon.aweme_detail(data)


class UserDetailView(HTTPMethodView):
    """
    用户详情
    """
    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        lemon = BaseLemon(request)
        return await lemon.user_detail(data)


class UserPostView(HTTPMethodView):
    """
    用户发布
    """
    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        lemon = BaseLemon(request)
        return await lemon.user_post(data)