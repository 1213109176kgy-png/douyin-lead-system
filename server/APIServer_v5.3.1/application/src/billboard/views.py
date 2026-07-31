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
@Date    ：2024/11/14 21:26
'''
from sanic import Request, HTTPResponse

from application.src.billboard.client.core import BaseView
from core import CustomException


class BillboardCategoryView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "billboard_type": data.get("billboard_type", "rise"),
            "type": "snapshot"
        }
        return await self.fetch_data(request, self.URL_MAPPING["billboard_category"], params=params,
                                     proxy=data.get("proxy"))


class UpBillboardView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 10),
            "sentence_tag": data.get("sentence_tag"),
            "order": data.get("order", "rank")
        }
        return await self.fetch_data(request, self.URL_MAPPING["up_hot"], params=params, proxy=data.get("proxy"))


class CityValueView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        return await self.fetch_data(request, self.URL_MAPPING["city_value"], proxy=data.get("proxy"))


class CityBillboardView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 10),
            "sentence_tag": data.get("sentence_tag"),
            "order": data.get("order", "rank"),
            "city_code": data.get("city_code")
        }
        return await self.fetch_data(request, self.URL_MAPPING["city_billboard"], params=params,
                                     proxy=data.get("proxy"))


class ChallengeBillboardView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 10)
        }
        return await self.fetch_data(request, self.URL_MAPPING["challenge_billboard"], params=params,
                                     proxy=data.get("proxy"))


class TotalBillboardView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 10),
            "sentence_tag": data.get("sentence_tag")
        }
        return await self.fetch_data(request, self.URL_MAPPING["total_billboard"], params=params,
                                     proxy=data.get("proxy"))


class SentenceVideoView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        sentence_id = data.get("sentence_id")
        if not sentence_id:
            raise CustomException(message="缺少sentence_id参数")
        params = {
            "page": data.get("page", 1),
            "page_size": data.get("page_size", 30)
        }
        endpoint = f"{self.URL_MAPPING['sentence_video']}{sentence_id}/sentence_item"
        return await self.fetch_data(request, endpoint, params=params, proxy=data.get("proxy"))


class UserFansDataView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        sec_uid = data.get("sec_uid")
        if not sec_uid:
            raise CustomException(message="缺少sec_uid参数")
        params = {
            "sec_uid": sec_uid,
            "option": data.get("option", "4")
        }
        return await self.fetch_data(request, self.URL_MAPPING["user_fans_data"], params=params,
                                     proxy=data.get("proxy"))


class UserFansInterestView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        sec_uid = data.get("sec_uid")
        interest_type = data.get("type")
        if not sec_uid or not interest_type or interest_type not in ['user_portrait', 'similar_author',
                                                                     'interest_topic', 'search']:
            raise CustomException(message="请求参数错误")
        if interest_type != 'user_portrait':
            interest_type = f'fans_interest/{interest_type}'
        endpoint = f"{self.URL_MAPPING['user_fans_interest']}{interest_type}"
        params = {
            "sec_uid": sec_uid
        }
        return await self.fetch_data(request, endpoint, params=params, proxy=data.get("proxy"))


class VideoDigsDataView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        aweme_id = data.get("aweme_id")
        option = data.get("option")
        if not aweme_id or not option:
            raise CustomException(message="缺少请求参数")
        params = {
            "option": option
        }
        endpoint = f"{self.URL_MAPPING['aweme_digs_data']}/{aweme_id}/item_portrait"
        return await self.fetch_data(request, endpoint, params=params, proxy=data.get("proxy"))


class VideoHotSpotDataView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        date_window = data.get("date")
        page = data.get("page")
        page_size = data.get("page_size")
        sub_type = data.get("sub_type")
        root_tag = data.get("root_tag")
        sub_tag = data.get("sub_tag")
        if not date_window or not page or not page_size or not sub_type:
            raise CustomException(message="缺少请求参数")
        request_json = {
            "date_window": date_window,
            "page": page,
            "page_size": page_size,
            "sub_type": sub_type,
            "tag_version": "v2"
        }
        if root_tag and sub_tag:
            request_json.update({
                "tags": [{
                    "value": root_tag,
                    "children": []
                }]
            })
            for i in sub_tag:
                request_json['tags'][0]['children'].append({"value": i})
        return await self.fetch_data(request, self.URL_MAPPING["hot_spot_video"], json_data=request_json,
                                     proxy=data.get("proxy"))


class VideoHotSpotCategoryView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        params = {
            "sort_key": "category_priority",
        }
        return await self.fetch_data(request, self.URL_MAPPING["hot_spot_category"], params=params,
                                     proxy=data.get("proxy"))


class MonitorUserView(BaseView):
    async def process_request(self, request: Request, data) -> HTTPResponse:
        date_window = data.get("date")
        page = data.get("page_num")
        page_size = data.get("page_size")
        root_tag = data.get("root_tag")
        sub_tag = data.get("sub_tag")
        if not date_window or not page or not page_size:
            raise CustomException(message="缺少请求参数")
        request_json = {
            "date_window": date_window,
            "monitor_status": 0,
            "order_by": 1,
            "page_num": page,
            "page_size": page_size,
            "platform": "web",
            "tag_version": "v2"
        }
        if root_tag and sub_tag:
            request_json.update({
                "query_tag": {
                    "value": root_tag,
                    "children": []
                }
            })
            for i in sub_tag:
                request_json['query_tag']['children'].append({"value": i})
        return await self.fetch_data(request, self.URL_MAPPING["monitor_user"], json_data=request_json,
                                     proxy=data.get("proxy"))
