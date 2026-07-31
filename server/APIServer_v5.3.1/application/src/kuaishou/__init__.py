#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/19 9:33 
'''
from sanic import Blueprint

from application.src.kuaishou.views import AwemeDetailView, AwemeDetailAppView, AwemeCommentView, UserNewPostView, \
    UserDetailV2View, UserPostView, UserInfoView, SearchAwemeView, AwemeShareLinkView, AwemeSubCommentView, \
    HotBillboardView, HotBillboardV2View, UserDetailV3View, UserPostV3View, UserShareLinkView

routes = {
    'aweme_detail': (AwemeDetailView.as_view(), "获取视频详情"),
    'aweme_detail_app': (AwemeDetailAppView.as_view(), "获取视频详情app"),
    'video_comment': (AwemeCommentView.as_view(), "获取视频评论"),
    'video_sub_comment': (AwemeSubCommentView.as_view(), "获取视频子评论"),
    'user_post': (UserPostView.as_view(), "获取用户发布"),
    'user_post_v3': (UserNewPostView.as_view(), "获取用户最新发布"),
    'user_post_v4': (UserPostV3View.as_view(), "获取用户主页发布"),
    'user_data': (UserInfoView.as_view(), "获取用户基本信息"),
    'user_data_v2': (UserDetailV2View.as_view(), "获取用户基本信息_v2"),
    'user_data_v3': (UserDetailV3View.as_view(), "获取用户基本信息_v3"),
    'search_aweme': (SearchAwemeView.as_view(), "搜索视频"),
    'user_share_link': (UserShareLinkView.as_view(), "用户短连接"),
    'aweme_share_link': (AwemeShareLinkView.as_view(), "视频短连接"),
    'hot_billboard': (HotBillboardView.as_view(), "热搜"),
    'hot_billboard_v2': (HotBillboardV2View.as_view(), "热搜v2"),
}

KUAISHOU_ROUTER = Blueprint('ks', url_prefix='ks')

# 注册路由
for path, (handler, name) in routes.items():
    KUAISHOU_ROUTER.add_route(handler, path, name=name)