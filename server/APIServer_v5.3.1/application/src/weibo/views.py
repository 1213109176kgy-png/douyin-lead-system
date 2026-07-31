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
@Date    ：2024/11/15 13:44 
@WebSite ：
'''
import re

from sanic import Request, HTTPResponse

from application.src.weibo.client.core import BaseView, RequestHandler, URLS, MOBILE_HEADERS
from core import CustomException, json_success_response


class UserDetailView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        uid = data.get("uid")
        share_text = data.get("share_text")
        if not uid and not share_text:
            raise CustomException()
        if not uid:
            uid = await RequestHandler.get_user_id(share_text)
        params = {
            "jumpfrom": "weibocom",
            "type": "uid",
            "value": uid,
            "containerid": f"100505{uid}",
        }
        headers = MOBILE_HEADERS.copy()
        cookie = await RequestHandler.get_cookie(request)
        headers.update({
            "cookie":f"_T_WM=37304392348; XSRF-TOKEN=ca7d3e; WEIBOCN_FROM=1110005030; mweibo_short_token=98d8960125; M_WEIBOCN_PARAMS=fid%3D1076031699432410%26uicode%3D10000011;{cookie}"
        })
        result = await RequestHandler.fetch_data(request, URLS["USER_DATA"], params, headers=headers)
        return json_success_response(result.get('data', {}).get('userInfo', {}))


class UserPostView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        uid = data.get("uid")
        share_text = data.get("share_text")
        page = data.get("page")
        if not uid and not share_text:
            raise CustomException()
        if not uid:
            uid = await RequestHandler.get_user_id(share_text)
        params = {
            "jumpfrom": "weibocom",
            "type": "uid",
            "value": uid,
            "containerid": f"107603{uid}",
            "page": page
        }
        headers = MOBILE_HEADERS.copy()
        cookie = await RequestHandler.get_cookie(request)
        headers.update({
            "cookie": f"_T_WM=37304392348; XSRF-TOKEN=ca7d3e; WEIBOCN_FROM=1110005030; mweibo_short_token=98d8960125; M_WEIBOCN_PARAMS=fid%3D1076031699432410%26uicode%3D10000011;{cookie}"
        })
        result = await RequestHandler.fetch_data(request, URLS["USER_POST"], params, headers=headers)
        return json_success_response(result)


class PostDetailView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        id = data.get("id")
        share_text = data.get("share_text")
        SUB = data.get("sub") or await RequestHandler.get_sub(request)
        if not id and not share_text:
            raise CustomException()
        if not id:
            id = await RequestHandler.get_post_id(share_text)
        params = {"id": id, "locale": "zh-CN", "isGetLongText": True}
        data = await RequestHandler.request_data(request, URLS["POST_DETAIL"], params, None, f"SUB={SUB}")
        return json_success_response(data)


class PostCommentView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        id = data.get("id")
        share_text = data.get("share_text")
        max_id = data.get("max_id")
        flow = data.get("flow", 0)
        SUB = data.get("sub") or await RequestHandler.get_sub(request)
        if not id and not share_text:
            raise CustomException()
        if not id:
            id = await RequestHandler.get_post_id(share_text)
        params = {"flow": flow, "is_reload": 1, "is_show_bulletin": 2, "is_mix": 0, "count": 10, "fetch_level": 0,
                  "locale": "zh-CN", "max_id": max_id, "id": id}
        result = await RequestHandler.request_data(request, URLS["POST_COMMENT"], params, None, f"SUB={SUB}")
        return json_success_response(result)


class PostSubCommentView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        id = data.get("id")
        max_id = data.get("max_id")
        flow = data.get("flow", 0)
        SUB = data.get("sub") or await RequestHandler.get_sub(request)
        if not id:
            raise CustomException()
        params = {"flow": flow, "is_reload": 1, "is_show_bulletin": 2, "is_mix": 1, "count": 10, "fetch_level": 1,
                  "locale": "zh-CN", "max_id": max_id, "id": id}
        result = await RequestHandler.request_data(request, URLS["POST_COMMENT"], params, None, f"SUB={SUB}")
        return json_success_response(result)


class TopicDetailView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        name = data.get("name")
        page = data.get("page", 1)
        if not name:
            raise CustomException()
        params = {"containerid": f"231522type=1&t=10&q=#{name}#", "page_type": "searchall",
                  "sudaref": "login.sina.com.cn", "isnewpage": 1, "page": page}
        headers = MOBILE_HEADERS.copy()
        cookie = await RequestHandler.get_cookie(request)
        headers.update({
            "cookie": f"_T_WM=37304392348; XSRF-TOKEN=ca7d3e; WEIBOCN_FROM=1110005030; mweibo_short_token=98d8960125; M_WEIBOCN_PARAMS=fid%3D1076031699432410%26uicode%3D10000011;{cookie}"
        })
        result = await RequestHandler.request_data(request, URLS["TOPIC_DETAIL"], params, headers=headers)
        return json_success_response(result)


class TopicStaticsView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        name = data.get("name")
        if not name:
            raise CustomException()
        detail_params = {"q": f"#{name}#", "show_rank_info": 1}
        trend_params = {"q": f"#{name}#", "version": "v1", "time": "24h"}
        headers = MOBILE_HEADERS.copy()
        detail_data = await RequestHandler.request_data(request, URLS["TOPIC_DETAIL_URL"], detail_params, None)
        trend_data = await RequestHandler.request_data(request, URLS["TOPIC_TREND_URL"], trend_params, None,
                                                       headers=headers)
        return json_success_response(
            {"topic_detail": detail_data.get('data', {}), "topic_trend": trend_data.get('data', {})})


class ShortVideoData(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        id = data.get("id")
        if not id:
            video_url = data.get("share_text")
            fid_value = re.search(r'fid=(\d+:\d+)', video_url)
            if not fid_value:
                raise CustomException()
            fid_value = fid_value.group(1)
        else:
            fid_value = id
        url = URLS["SHORT_VIDEO_URL"] + fid_value
        request_data = {
            "data": '{"Component_Play_Playinfo":{"oid":"' + fid_value + '"}}'
        }
        response = await RequestHandler.request_data(request, url, {}, data=request_data)
        return json_success_response(response)


class SearchDataView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        keyword = data.get("keyword")
        page = data.get("page") or "1"
        type = data.get("type") or "1"
        if not keyword:
            raise CustomException()
        params = {
            "containerid": f"100103type={str(type)}&q={keyword}&t=",
            "page": str(page),
            "page_type": "searchall"
        }
        # SUB = data.get("sub") or await RequestHandler.get_sub(request)
        headers = MOBILE_HEADERS.copy()
        cookie = await RequestHandler.get_cookie(request)
        headers.update({
            "cookie": f"_T_WM=37304392348; XSRF-TOKEN=ca7d3e; WEIBOCN_FROM=1110005030; mweibo_short_token=98d8960125; M_WEIBOCN_PARAMS=fid%3D1076031699432410%26uicode%3D10000011;{cookie}"
        })
        result = await RequestHandler.fetch_data(request, url=URLS["SEARCH_URL"], params=params, headers=headers)
        return json_success_response(result)


class UserVideoView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        uid = data.get("uid")
        share_text = data.get("share_text")
        SUB = data.get("sub") or await RequestHandler.get_sub(request)
        if not uid and not share_text:
            raise CustomException()
        if not uid:
            uid = await RequestHandler.get_user_id(share_text)
        params = {"uid": uid}
        result = await RequestHandler.request_data(request, URLS["USER_VIDEO_POST"], params, None, f"SUB={SUB}")
        return json_success_response(result)


class HotSearchView(BaseView):
    async def handle_request(self, request: Request, data: dict) -> HTTPResponse:
        hot_type = data.get("hot_type")

        if hot_type == "hot":
            url = "https://weibo.com/ajax/side/hotSearch"
        elif hot_type == "entertainment":
            url = "https://weibo.com/ajax/statuses/entertainment"
        elif hot_type == "life":
            url = "https://weibo.com/ajax/statuses/life"
        elif hot_type == "social":
            url = "https://weibo.com/ajax/statuses/social"
        else:
            raise CustomException(message="请传入热搜类型")
        result = await RequestHandler.request_data(request, url, {}, None)
        return json_success_response(result)
