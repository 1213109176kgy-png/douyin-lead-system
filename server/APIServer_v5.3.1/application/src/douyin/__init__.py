#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/8 9:15 
'''
from sanic import Blueprint

from application.src.douyin.views import AwemeDetailView, MultipleAwemeDetailView, AwemeDetailV3View, AwemeDetailV4View, \
    UserDetailView, UserDetailV2View, UserDetailV3View, UserDetailV4View, UserDetailByUIDView, UserDetailByShortIDView, \
    UserPostView, UserNewPostView, UserMixView, MixInfoView, MixAwemeListView, SearchUserAwemeView, UserFavView, \
    AwemeRootCommentsView, AwemeSubCommentsView, UserSeriesView, SeriesInfoView, SeriesAwemeListView, \
    GeneralSearchV2View, SearchVideoView, SearchUserV2View, SearchMusicView, MusicInfoView, MusicAwemeListView, \
    SearchHashtagView, HashTagInfoView, HashTagAwemeListView, HashTagAwemeListV2View, GeneralSearchView, \
    SearchVideoV2View, SearchLiveUserView, LiveRoomInfoByRidView, LiveRoomInfoByIdView, CheckUserLiveStatusView, \
    LiveRoomUserListView, AwemeDanmakuView, UserShortLinkView, AwemeShortLinkView, AwemeQRCodeView, SearchSlugView, \
    SentenceView, SchemeView, AwemeListNearByView, LiveListNearByView, AwemeFansCountView, UserTagView, \
    UserProductDataView, SearchUserView, GeneralSearchStreamView, GeneralSearchAccountView, MediumChannelFeedView, \
    AwemeBoardView, SearchHashtagV2View, AwemeShortenView, GetAnonymousCookie, SearchLiveUserV2View, WeekSelectView, \
    SearchUserV3View, UserPostV2View, GeneralSearchV3View, SearchVideoV3View, IndexFeedView, SearchHotValueView

routes = {
    'aweme_detail': (AwemeDetailView.as_view(), "获取视频详情"),
    'aweme_detail_v3': (AwemeDetailV3View.as_view(), "获取视频详情_v3"),
    'aweme_detail_v4': (AwemeDetailV4View.as_view(), "获取视频详情_v4"),
    'multiple_aweme_detail': (MultipleAwemeDetailView.as_view(), "批量获取视频详情"),
    'aweme_new_fans_count': (AwemeFansCountView.as_view(), "获取视频涨粉数量"),
    'user_data': (UserDetailView.as_view(), "获取用户信息"),
    'user_data_v2': (UserDetailV2View.as_view(), "获取用户信息_v2"),
    'user_data_v3': (UserDetailV3View.as_view(), "获取用户信息_v3"),
    'user_data_v4': (UserDetailV4View.as_view(), "获取用户信息_v4"),
    'user_data_by_uid': (UserDetailByUIDView.as_view(), "通过UID获取用户信息"),
    'user_data_by_short': (UserDetailByShortIDView.as_view(), "通过抖音号获取用户信息"),
    'user_tag': (UserTagView.as_view(), "获取用户标签"),
    'user_post': (UserPostView.as_view(), "获取用户主页发布"),
    'user_post_v2': (UserPostV2View.as_view(), "获取用户主页发布_v2"),
    'user_post_v3': (UserNewPostView.as_view(), "获取用户最新发布"),
    'user_product_data': (UserProductDataView.as_view(), "获取用户主页作品分析数据"),
    'user_mix': (UserMixView.as_view(), "获取用户合集"),
    'user_mix_info': (MixInfoView.as_view(), "获取合集信息"),
    'user_mix_aweme_list': (MixAwemeListView.as_view(), "获取合集视频列表"),
    'search_user_aweme': (SearchUserAwemeView.as_view(), "搜索用户指定作品"),
    'user_favorite': (UserFavView.as_view(), "获取用户喜欢的作品"),
    'video_comment': (AwemeRootCommentsView.as_view(), "获取视频一级评论"),
    'video_sub_comment': (AwemeSubCommentsView.as_view(), "获取视频二级评论"),
    'user_series_list': (UserSeriesView.as_view(), "获取用户短剧集"),
    'series_detail': (SeriesInfoView.as_view(), "获取短剧详细信息"),
    'series_aweme_list': (SeriesAwemeListView.as_view(), "获取短剧视频列表"),
    'general_search': (GeneralSearchView.as_view(), "综合搜索"),
    'search_account': (GeneralSearchAccountView.as_view(), "获取搜索cookie"),
    'general_search_stream': (GeneralSearchStreamView.as_view(), "综合搜索Stream"),
    'general_search_v2': (GeneralSearchV2View.as_view(), "综合搜索v2"),
    'general_search_v3': (GeneralSearchV3View.as_view(), "综合搜索v3"),
    'search_video': (SearchVideoView.as_view(), "搜索视频"),
    'search_video_v2': (SearchVideoV2View.as_view(), "搜索视频_v2"),
    'search_video_v3': (SearchVideoV3View.as_view(), "搜索视频_v3"),
    'search_user': (SearchUserView.as_view(), "搜索用户"),
    'search_user_v2': (SearchUserV2View.as_view(), "搜索用户v2"),
    'search_user_v3': (SearchUserV3View.as_view(), "搜索用户v3"),
    'search_music': (SearchMusicView.as_view(), "搜索音乐"),
    'music_detail': (MusicInfoView.as_view(), "获取音乐详情"),
    'music_aweme': (MusicAwemeListView.as_view(), "获取音乐相关视频"),
    'search_topic': (SearchHashtagView.as_view(), "搜索话题"),
    'search_topic_v2': (SearchHashtagV2View.as_view(), "搜索话题v2"),
    'challenge_detail': (HashTagInfoView.as_view(), "获取话题详情"),
    'topic_data': (HashTagAwemeListView.as_view(), "获取话题视频"),
    'topic_data_v2': (HashTagAwemeListV2View.as_view(), "获取话题视频v2"),
    'search_live': (SearchLiveUserView.as_view(), "搜索直播用户"),
    'search_live_v2': (SearchLiveUserV2View.as_view(), "搜索直播用户_v2"),
    'live_room_data': (LiveRoomInfoByRidView.as_view(), "通过web_rid获取直播间信息"),
    'live_room_by_id': (LiveRoomInfoByIdView.as_view(), "通过room_id获取直播间信息"),
    'check_user_live_status': (CheckUserLiveStatusView.as_view(), "检查用户直播状态"),
    'live_user_data': (LiveRoomUserListView.as_view(), "获取开放直播间用户列表"),
    'aweme_danmaku': (AwemeDanmakuView.as_view(), "获取视频弹幕"),
    'user_short_link': (UserShortLinkView.as_view(), "获取用户主页短连接"),
    'aweme_short_link': (AwemeShortLinkView.as_view(), "获取视频短连接"),
    'aweme_qr_code': (AwemeQRCodeView.as_view(), "生成视频抖音码"),
    'search_sug': (SearchSlugView.as_view(), "搜索长尾关键词"),
    'hot_spot_aladdin': (SentenceView.as_view(), "热点讨论"),
    'share_to_scheme': (SchemeView.as_view(), "获取协议链接"),
    'near_by': (AwemeListNearByView.as_view(), "获取同城视频"),
    'live_room_by_map': (LiveListNearByView.as_view(), "获取同城直播"),
    'medium_channel_feed': (MediumChannelFeedView.as_view(), "精选内容"),
    'aweme_board': (AwemeBoardView.as_view(), "抖音热点榜"),
    'aweme_shorten': (AwemeShortenView.as_view(), "短连接"),
    'get_anonymous_cookie': (GetAnonymousCookie.as_view(), "匿名cookie获取"),
    'week_select': (WeekSelectView.as_view(), "每周精选视频"),
    'index_feed': (IndexFeedView.as_view(), "首页推荐"),
    'search_kwd_value': (SearchHotValueView.as_view(), "关键词热度排行"),
}

DOUYIN_ROUTER = Blueprint('douyin', url_prefix='douyin')

# 注册路由
for path, (handler, name) in routes.items():
    DOUYIN_ROUTER.add_route(handler, path, name=name)