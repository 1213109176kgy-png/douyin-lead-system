#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 13:27 
'''
from sanic import Blueprint

from application.src.toutiao.views import VideoDetailView, ArticleDetailView, ArticleRootCommentView, \
    ArticleSubCommentView, UserPostList, VideoDetailV2View, ArticleInformation

toutiao_routes = {
    'aweme_detail': (VideoDetailView.as_view(), "获取头条视频详情"),
    'aweme_detail_v2': (VideoDetailV2View.as_view(), "获取头条视频详情v2"),
    'article_detail': (ArticleDetailView.as_view(), "获取头条文章详情"),
    'article_root_comment': (ArticleRootCommentView.as_view(), "获取头条文章父评论"),
    'article_sub_comment': (ArticleSubCommentView.as_view(), "获取头条文章子评论"),
    'user_post': (UserPostList.as_view(), "获取头条用户主页发布"),
    'article_information': (ArticleInformation.as_view(), "获取文章详情"),
}

TOUTIAO_ROUTER = Blueprint('toutiao', url_prefix='toutiao')

for path, (handler, name) in toutiao_routes.items():
    TOUTIAO_ROUTER.add_route(handler, path, name=name)