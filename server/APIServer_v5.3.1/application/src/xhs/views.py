#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 9:57 
'''
import traceback
from loguru import logger
from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.xhs.client.base import BaseClient
from core import json_fail_response, CustomException, json_success_response


class BaseAPIView(HTTPMethodView):
    async def dispatch_request(self, request, *args, **kwargs):
        method_name = request.method.lower()
        handler = getattr(self, method_name, None)
        api_name = self.__class__.__name__
        try:
            if handler:
                response = await handler(request, *args, **kwargs)
                return response
            else:
                logger.warning(f"不支持的请求方法: {request.method} - {api_name}")
                return json_fail_response(code=405, message=f"方法 '{request.method}' 不被允许")

        except CustomException as e:
            logger.warning(f"业务异常: {api_name} - {str(e)}")
            raise e
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"系统异常: {api_name} - {str(e)}\n{error_details}")
            raise CustomException(message=f"服务器处理请求时发生错误: {str(e)}")


class NoteDetailView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.note_detail()
        return json_success_response(response)


class NoteDetailV2View(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.note_detail_v2()
        return json_success_response(response)


class NoteDetailV3View(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.note_detail_v3()
        return json_success_response(response)


class UserDetailView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.user_detail()
        return json_success_response(response)

class UserDetailV2View(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.user_detail_v2()
        return json_success_response(response)


class AnyAccountView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.any_account()
        return json_success_response(response)


class UserPostView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.user_post()
        return json_success_response(response)


class SearchNoteView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.search_note()
        return json_success_response(response)


class SearchUserView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.search_user()
        return json_success_response(response)


class SearchOneBoxView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.search_one_box()
        return json_success_response(response)


class SearchTopicView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.search_topic()
        return json_success_response(response)


class NoteRootCommentView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.note_root_comment()
        return json_success_response(response)


class NoteSubCommentView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.note_sub_comment()
        return json_success_response(response)


class HomeFeedView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.home_feed()
        return json_success_response(response)


class SearchSuggestView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.search_suggest()
        return json_success_response(response)


class QrCodeView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.qr_code()
        return json_success_response(response)


class CheckQrCodeView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.check_qr_code()
        return json_success_response(response)


class QrCodeCaptchaInitView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.qr_code_captcha_init()
        return json_success_response(response)


class QueryQRCodeView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.query_qr_code_captcha()
        return json_success_response(response)



class MobileLoginSendCode(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.mobile_login_send_code()
        return json_success_response(response)


class MobileLoginCheckCode(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.mobile_login_check_code()
        return json_success_response(response)


class MobileLoginCheckStatus(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.mobile_login_check_status()
        return json_success_response(response)


class MobileLoginQRCode(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.mobile_login_qr_code()
        return json_success_response(response)


class MobileLoginCheckQRCode(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.mobile_login_check_qr_code()
        return json_success_response(response)

class MeInfoView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.me_info()
        return json_success_response(response)


class MeInfoV2View(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.get_me_info_v2()
        return json_success_response(response)


class AtsCommentsListView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.ats_comment()
        return json_success_response(response)


class LikesListView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.likes()
        return json_success_response(response)


class ConnectionsView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.connections()
        return json_success_response(response)


class ShareCodeView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.share_code()
        return json_success_response(response)


class ShortLinkView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.short_link()
        return json_success_response(response)


class ViewNoteView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.view_note()
        return json_success_response(response)


class GetCreatorCookieView(BaseAPIView):
    async def post(self, request: Request) -> HTTPResponse:
        client = BaseClient(request)
        response = await client.get_creator_cookie()
        return json_success_response(response)