#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：init.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 9:31 
'''
from sanic import Blueprint

from application.src.bilibili.views import AwemeDetailView, AwemeCardDetailView, AwemeDownloadView, UserALLPostView, \
    UserALLPostV2View, SearchView, CommentsDataView, UserInfoView, UserVideoListView, DownloadViewV2View, \
    GetOpusDetailView, PopularView, RankView, AwemeDetailV2View

routes = {
    'video_data': (AwemeDetailView.as_view(), "获取视频信息"),
    'video_data_v2': (AwemeCardDetailView.as_view(), "获取视频选集信息"),
    'video_data_v3': (AwemeDetailV2View.as_view(), "获取视频信息v2"),
    'video_download': (AwemeDownloadView.as_view(), "视频下载"),
    'user_post': (UserALLPostView.as_view(), "获取用户所有动态"),
    'user_post_v2': (UserALLPostV2View.as_view(), "获取用户所有动态v2"),
    'search': (SearchView.as_view(), "搜索数据"),
    'comments': (CommentsDataView.as_view(), "获取视频评论"),
    'user_info': (UserInfoView.as_view(), "获取用户信息"),
    'user_videos': (UserVideoListView.as_view(), "获取用户投稿视频"),
    'video_download_v2': (DownloadViewV2View.as_view(), "视频下载v2"),
    'opus_info': (GetOpusDetailView.as_view(), "获取图文信息"),
    'popular': (PopularView.as_view(), "综合热门"),
    'rank': (RankView.as_view(), "排行榜"),
}

BILIBILI_ROUTER = Blueprint('bilibili', url_prefix='bilibili')

# 注册路由
for path, (handler, name) in routes.items():
    BILIBILI_ROUTER.add_route(handler, path, name=name)