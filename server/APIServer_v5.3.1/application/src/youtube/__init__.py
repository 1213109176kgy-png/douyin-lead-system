# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 13:52 
@WebSite ：
'''
from sanic import Blueprint

from application.src.youtube.views import AwemeDetailView, VideoCommentView, SearchDataView, PlaylistsView, \
    PlaylistItemsView, GetChannelIDView, UserPostView, CommentListView

routes = {
    'video_data': (AwemeDetailView.as_view(), "获取视频信息"),
    'video_comment': (VideoCommentView.as_view(), "获取视频评论"),
    'search_data': (SearchDataView.as_view(), "搜索数据"),
    'play_list': (PlaylistsView.as_view(), "获取频道播放列表"),
    'play_list_item': (PlaylistItemsView.as_view(), "获取播放列表视频"),
    'get_channel_id': (GetChannelIDView.as_view(), "获取用户channelID"),
    'user_post': (UserPostView.as_view(), "获取用户发布"),
    'comment_list': (CommentListView.as_view(), "获取评论列表"),

}

YOUTUBE_ROUTER = Blueprint('youtube', url_prefix='youtube')

for path, (handler, name) in routes.items():
    YOUTUBE_ROUTER.add_route(handler, path, name=name)