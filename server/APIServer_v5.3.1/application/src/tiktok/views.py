#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 

@Date    ：2025/4/22 10:31 
'''
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.tiktok.client.base import TikTokBase


class AwemeDetailView(HTTPMethodView):
    """
    获取单一作品详情
    """

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.aweme_detail(request)


class UserDetailView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.user_detail(request)


class AwemeRootCommentView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.aweme_root_comments(request)


class AwemeSubCommentView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.aweme_sub_comment(request)


class UserPostView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.user_post(request)


class GeneralSearchView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.general_search(request)


class SearchUserView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.search_user(request)


class SearchItemView(HTTPMethodView):

    async def post(self, request: Request) -> HTTPResponse:
        tiktok = TikTokBase(request)
        return await tiktok.search_item(request)