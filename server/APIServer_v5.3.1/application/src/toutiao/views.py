# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 11:48 
@WebSite ：
'''
from application.src.toutiao.client.core import BaseView


class VideoDetailView(BaseView):
    """
    处理视频详情的视图
    """
    handler_method = 'video_detail'


class VideoDetailV2View(BaseView):
    """
    处理视频详情v2的视图
    """
    handler_method = 'video_detail_v2'


class ArticleDetailView(BaseView):
    """
    处理文章详情的视图
    """
    handler_method = 'article_detail'


class ArticleRootCommentView(BaseView):
    """
    获取文章父级评论
    """
    handler_method = "article_root_comment"


class ArticleSubCommentView(BaseView):
    """
    获取文章父级评论
    """
    handler_method = "article_sub_comment"


class UserPostList(BaseView):
    """
    获取用户主页发布
    """
    handler_method = 'user_post'


class ArticleInformation(BaseView):
    """
    头条文章
    """
    handler_method = 'article_information'
