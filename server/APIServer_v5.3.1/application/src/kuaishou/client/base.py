#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：base.py
@IDE     ：PyCharm 

@Date    ：2025/4/19 9:55 
'''
import json
import re

from application.src.kuaishou.args.sig import get_payload
from core import CustomException
from libs import get_request_proxy, get_request_data
from libs.common import extract_url


class KwBase:
    def __init__(self, request):
        self.request = request

    async def get_request_data(self):
        return await get_request_data(self.request)

    async def _extract_url(self, text: str):
        return await extract_url(text)

    async def _proxy(self):
        return await get_request_proxy(self.request)

    async def _http_request(self, url: str, headers: dict, params: dict = None, data: dict = None, json: dict=None, proxy: str = None,
                            allow_redirects: bool = True, request_method: str = "GET"):

        if request_method == "GET":
            response = await self.request.app.ctx.curl_client.http_get(url=url, params=params, headers=headers,
                                                                       proxy=proxy,
                                                                       allow_redirects=allow_redirects)
            return response
        else:
            response = await self.request.app.ctx.curl_client.http_post(url=url, params=params, headers=headers,
                                                                        proxy=proxy,
                                                                        data=data,
                                                                        json=json,
                                                                        allow_redirects=allow_redirects)
            return response

    def find_photo(self, d):
        profiles = []
        found_dict = False
        if isinstance(d, dict):
            found_dict = True
            for key, value in d.items():
                if key == "photo" and isinstance(value, dict):
                    profiles.append(value)
                # Recursively process the value
                result = self.find_photo(value)
                if result is not None:
                    profiles.extend(result)
                    found_dict = True
        elif isinstance(d, list):
            for item in d:
                result = self.find_photo(item)
                if result is not None:
                    profiles.extend(result)
                    found_dict = True
        return profiles if found_dict else None


    async def _detail_init_state(self, text:str):
        r_text = r'<script>window\.INIT_STATE = (.*?)</script>'
        match = re.search(r_text, text, re.DOTALL)
        wid_value = match.group(1)
        res = json.loads(wid_value)
        result = self.find_photo(res) if self.find_photo(res) else None
        return result

    async def get_photos(self, text:str):
        try:
            if type(text) is list:
                photo_id_list = []
                for i in text:
                    photo_id_list.append({"photoId": i})
            else:
                photo_id_list = [{"photoId": text}]
            photo_ids = json.dumps(photo_id_list)
            return photo_ids
        except Exception as e:
            raise CustomException(message=f"id参数错误 {str(e)}")


    async def sig_data(self, url, payload):
        _sig = await get_payload(http_client=self.request.app.ctx.curl_client, url=url, payload=payload)
        return _sig

    def _extract_keys(self, d):
        result = {}
        if isinstance(d, dict):
            for key, value in d.items():
                if key in ["result", "feeds", "pcursor", "llsid"]:
                    result[key] = value
                elif isinstance(value, dict):
                    result.update(self._extract_keys(value))
                elif isinstance(value, list):
                    for item in value:
                        result.update(self._extract_keys(item))
        return result

    async def find_user_profiles(self, d):
        profiles = []
        if isinstance(d, dict):
            for key, value in d.items():
                if key == "userProfile":
                    profiles.append(value)
                profiles.extend(await self.find_user_profiles(value))
        elif isinstance(d, list):
            for item in d:
                profiles.extend(await self.find_user_profiles(item))
        return profiles

    async def remove_dict_with_fid(self, data_list, fid_value):
        for item in data_list:
            if isinstance(item, dict) and str(item['profile']['user_id']) == fid_value:
                data_list.remove(item)
                break
        # 返回列表中的唯一字典
        return data_list[0] if data_list else None

    def extract_vision_hot_rank_items(self, input_str):
        pattern = r'"VisionHotRankItem:[^"]+":\s*({(?:[^{}]|(?:\{[^{}]*\})*)*})'
        matches = re.findall(pattern, input_str, re.DOTALL)

        items = []
        for match in matches:
            try:
                item = json.loads(match)
                items.append(item)
            except json.JSONDecodeError as e:
                pass
        return items
