#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 9:57 
'''
from sanic import Blueprint

from application.src.xhs.views import (
    NoteDetailView,
    UserDetailView,
    AnyAccountView,
    UserPostView,
    NoteDetailV2View,
    NoteDetailV3View, SearchNoteView, SearchUserView, NoteRootCommentView, NoteSubCommentView, HomeFeedView,
    SearchSuggestView, SearchTopicView, QrCodeView, CheckQrCodeView, MobileLoginSendCode, MobileLoginCheckCode,
    MobileLoginCheckStatus, MobileLoginQRCode, MobileLoginCheckQRCode, UserDetailV2View, MeInfoView, MeInfoV2View,
    LikesListView, ConnectionsView, ShareCodeView, ShortLinkView, AtsCommentsListView, SearchOneBoxView, ViewNoteView,
    QrCodeCaptchaInitView, QueryQRCodeView, GetCreatorCookieView
)

# API路由配置
routes = {
    'note_detail': (NoteDetailView.as_view(), "获取笔记详情"),
    'note_detail_v2': (NoteDetailV2View.as_view(), "获取笔记详情v2"),
    'note_detail_v3': (NoteDetailV3View.as_view(), "获取笔记详情v3"),
    'user_detail': (UserDetailView.as_view(), "获取用户详情"),
    'user_detail_v2': (UserDetailV2View.as_view(), "获取用户详情_v2"),
    'user_post': (UserPostView.as_view(), "获取用户发布的笔记列表"),
    'any_account': (AnyAccountView.as_view(), "获取匿名cookie"),
    'search_note': (SearchNoteView.as_view(), "搜索笔记"),
    'search_user': (SearchUserView.as_view(), "搜索用户"),
    'search_one_box': (SearchOneBoxView.as_view(), "根据小红书号搜索用户"),
    'search_topic': (SearchTopicView.as_view(), "搜索话题"),
    'note_comment': (NoteRootCommentView.as_view(), "获取笔记父评论"),
    'note_sub_comment': (NoteSubCommentView.as_view(), "获取笔记子评论"),
    'home_feeds': (HomeFeedView.as_view(), "获取首页推荐"),
    'search_suggestion': (SearchSuggestView.as_view(), "获取搜索联想词"),
    'login_qr_code': (QrCodeView.as_view(), "获取登录二维码"),
    'check_login': (CheckQrCodeView.as_view(), "检查二维码扫描结果"),
    'captcha_init': (QrCodeCaptchaInitView.as_view(), "初始化二维码"),
    'query_captcha': (QueryQRCodeView.as_view(), "检查验证二维码"),
    'send_code': (MobileLoginSendCode.as_view(), "手机登录-发送验证码"),
    'check_code': (MobileLoginCheckCode.as_view(), "手机登录-验证短信"),
    'login_code': (MobileLoginCheckStatus.as_view(), "手机登录-登录状态"),
    'login_code_verify_qr': (MobileLoginQRCode.as_view(), "手机登录-验证二维码"),
    'login_code_verify_query': (MobileLoginCheckQRCode.as_view(), "手机登录-验证扫码结果"),
    'me': (MeInfoView.as_view(), "获取登录的用户信息"),
    'me_v2': (MeInfoV2View.as_view(), "获取登录的用户信息_v2"),
    'mentions': (AtsCommentsListView.as_view(), "获取艾特和评论"),
    'likes': (LikesListView.as_view(), "获取赞和收藏"),
    'connections': (ConnectionsView.as_view(), "获取新增关注"),
    'share_code': (ShareCodeView.as_view(), "获取分享code"),
    'short_link': (ShortLinkView.as_view(), "获取短链"),
    'view_note': (ViewNoteView.as_view(), "看笔记"),
    'creator_cookie': (GetCreatorCookieView.as_view(), "创作者cookie"),
}

XHS_ROUTER = Blueprint('xhs', url_prefix='xhs')

# 注册路由
for path, (handler, name) in routes.items():
    XHS_ROUTER.add_route(handler, path, name=name)

# # 这些变量将被外部导入
# __all__ = ['XHS_ROUTER']