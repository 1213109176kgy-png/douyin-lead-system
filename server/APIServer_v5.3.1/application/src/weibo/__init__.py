#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/20 19:22 
'''
from sanic import Blueprint

from application.src.weibo.views import UserDetailView, UserVideoView, SearchDataView, ShortVideoData, TopicStaticsView, \
    TopicDetailView, PostSubCommentView, PostCommentView, PostDetailView, UserPostView, HotSearchView

routes = {
    'user_detail': (UserDetailView.as_view(), "获取用户信息"),
    'user_post': (UserPostView.as_view(), "获取用户发布"),
    'post_detail': (PostDetailView.as_view(), "获取微博详情"),
    'post_comment': (PostCommentView.as_view(), "获取微博评论"),
    'post_sub_comment': (PostSubCommentView.as_view(), "获取微博子评论"),
    'topic_detail': (TopicDetailView.as_view(), "获取话题详情"),
    'topic_statics': (TopicStaticsView.as_view(), "获取话题数据"),
    'short_video': (ShortVideoData.as_view(), "获取短视频信息"),
    'search_data': (SearchDataView.as_view(), "搜索"),
    'user_video': (UserVideoView.as_view(), "获取用户视频列表"),
    'hot_search': (HotSearchView.as_view(), "获取热搜"),
}

WEIBO_ROUTER = Blueprint('weibo', url_prefix='weibo')

# 注册路由
for path, (handler, name) in routes.items():
    WEIBO_ROUTER.add_route(handler, path, name=name)