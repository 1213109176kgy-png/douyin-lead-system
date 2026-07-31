#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 13:27 
'''
from sanic import Blueprint

from application.src.xigua.views import XGDetailView, XGUserInfoView, XGUserPostView, XGDetailV2View

routes = {
    'aweme_detail': (XGDetailView.as_view(), "获取西瓜视频详情"),
    'aweme_detail_v2': (XGDetailV2View.as_view(), "获取西瓜视频详情_v2"),
    'user_detail': (XGUserInfoView.as_view(), "获取西瓜用户信息"),
    'user_post': (XGUserPostView.as_view(), "获取西瓜用户主页发布"),
}

XIGUA_ROUTER = Blueprint('xigua', url_prefix='xigua')

for path, (handler, name) in routes.items():
    XIGUA_ROUTER.add_route(handler, path, name=name) 