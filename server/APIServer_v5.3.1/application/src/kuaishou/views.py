#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 

@Date    ：2025/4/19 9:33 
'''
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.kuaishou.client.core import KwCore
from core import json_success_response, CustomException


class AwemeDetailView(HTTPMethodView):
    """
    视频详情
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        share_text = request_data.get("share_text")
        data = await client.aweme_detail(share_text=share_text)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class AwemeDetailAppView(HTTPMethodView):
    """
    视频详情app
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        photo_id = request_data.get("photo_id")
        data = await client.aweme_detail_app(photo_id=photo_id)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class AwemeCommentView(HTTPMethodView):
    """
    视频评论
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        photo_id = request_data.get("aweme_id")
        pcursor = request_data.get("pcursor", "0")
        data = await client.aweme_comment(photo_id=photo_id, pcursor=pcursor)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class AwemeSubCommentView(HTTPMethodView):
    """
    视频子评论
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        photo_id = request_data.get("aweme_id")
        root_comment_id = request_data.get("root_comment_id")
        pcursor = request_data.get("pcursor", "0")
        data = await client.aweme_sub_comment(photo_id=photo_id, root_comment_id=root_comment_id, pcursor=pcursor)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class UserPostView(HTTPMethodView):
    """
    用户发布
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        user_id = request_data.get("user_id")
        pcursor = request_data.get("pcursor", "0")
        cookie = request_data.get("cookie", "")
        data = await client.user_post(user_id=user_id, pcursor=pcursor, cookie=cookie)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")




class UserNewPostView(HTTPMethodView):
    """
    用户最新发布
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        share_text = request_data.get("share_text")
        data = await client.user_post_v3(share_text=share_text)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")




class UserPostV3View(HTTPMethodView):
    """
    用户发布v3
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        user_id = request_data.get("user_id")
        pcursor = request_data.get("pcursor", "0")
        data = await client.user_post_app(user_id=user_id, pcursor=pcursor)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")




class UserInfoView(HTTPMethodView):
    """
    用户详情
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        user_id = request_data.get("user_id")
        cookie = request_data.get("cookie", "")
        data = await client.user_info(user_id=user_id, cookie=cookie)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")



class UserDetailV2View(HTTPMethodView):
    """
    用户详情
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        share_text = request_data.get("share_text")
        data = await client.user_info_v2(share_text=share_text)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")

class UserDetailV3View(HTTPMethodView):
    """
    用户详情v3
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        user_id = request_data.get("user_id")
        data = await client.user_info_v3(user_id=user_id)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")





class SearchAwemeView(HTTPMethodView):
    """
    搜索视频
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        keyword = request_data.get("keyword")
        pcursor = request_data.get("pcursor")
        cookie = request_data.get("cookie")
        data = await client.search_aweme(keyword=keyword, pcursor=pcursor, cookie=cookie)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class AwemeShareLinkView(HTTPMethodView):
    """
    短连接
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        photo_id = request_data.get("photo_id")
        data = await client.short_link(photo_id=photo_id)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class UserShareLinkView(HTTPMethodView):
    """
    用户短连接
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        user_id = request_data.get("user_id")
        data = await client.user_short_link(user_id=user_id)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")



class HotBillboardView(HTTPMethodView):
    """
    r热榜
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        data = await client.hot_billboard()
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")


class HotBillboardV2View(HTTPMethodView):
    """
    r热榜
    """
    async def post(self, request: Request) -> HTTPResponse:
        client = KwCore(request=request)
        request_data = await client.get_request_data()
        board_type = request_data.get("board_type", "1")
        data = await client.hot_billboard_v2(board_type)
        if data:
            return json_success_response(data)
        raise CustomException(message="数据获取失败")