#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/18 20:44 
'''
from sanic import Blueprint

from application.src.billboard.views import BillboardCategoryView, UpBillboardView, CityValueView, CityBillboardView, \
    ChallengeBillboardView, TotalBillboardView, SentenceVideoView, UserFansDataView, UserFansInterestView, \
    VideoDigsDataView, VideoHotSpotDataView, VideoHotSpotCategoryView, MonitorUserView

routes = {
    'billboard_category': (BillboardCategoryView.as_view(), "抖音热点分类"),
    'rise': (UpBillboardView.as_view(), "抖音实时上升热点榜"),
    'city_value': (CityValueView.as_view(), "抖音城市列表"),
    'city_billboard': (CityBillboardView.as_view(), "抖音同城热点榜单"),
    'challenge_billboard': (ChallengeBillboardView.as_view(), "抖音实时挑战榜"),
    'total_billboard': (TotalBillboardView.as_view(), "抖音热点总榜"),
    'billboard_video': (SentenceVideoView.as_view(), "抖音榜单相关视频"),
    'user_fans_data': (UserFansDataView.as_view(), "抖音用户粉丝画像"),
    'user_fans_interest': (UserFansInterestView.as_view(), "抖音用户粉丝兴趣"),
    'aweme_digs_interest': (VideoDigsDataView.as_view(), "抖音视频点赞观众画像"),
    'hot_spot_video': (VideoHotSpotDataView.as_view(), "抖音视频榜单"),
    'content_tag': (VideoHotSpotCategoryView.as_view(), "榜单垂直分类标签"),
    'monitor_user': (MonitorUserView.as_view(), "抖音热门账号"),
}

BILLBOARD_ROUTER = Blueprint('billboard', url_prefix='billboard')

# 注册路由
for path, (handler, name) in routes.items():
    BILLBOARD_ROUTER.add_route(handler, path, name=name)