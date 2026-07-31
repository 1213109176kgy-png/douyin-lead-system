#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：core.py
@IDE     ：PyCharm 

@Date    ：2025/4/19 9:55 
'''
import json
import re
from urllib.parse import urlparse, parse_qs

from application.src.kuaishou.client.base import KwBase
from application.src.kuaishou.client.parameter import aweme_detail_headers, aweme_detail_path, app_headers, \
    aweme_comment_path, base_user_post, base_headers, base_user_info, search_video_data, short_link_path, \
    aweme_sub_comment_path, home_url, hot_billboard_v2_path, user_info_v3_path, user_post_app_path, user_short_link_path
from core import CustomException


class KwCore(KwBase):
    base_url = "https://www.kuaishou.com/graphql"

    async def aweme_detail(self, share_text: str) -> dict:
        """
        视频详情
        """
        share_text = await self._extract_url(share_text)
        headers = await aweme_detail_headers()
        response = await self._http_request(url=share_text, headers=headers, allow_redirects=True,
                                            proxy=await self._proxy())
        result = await self._detail_init_state(response.text)
        return result

    async def aweme_detail_app(self, photo_id) -> dict:
        photo_id = await self.get_photos(photo_id)
        headers = await app_headers()
        url, payload = await aweme_detail_path(app=self.request.app,photo_ids=photo_id)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()

    async def aweme_comment(self, photo_id, pcursor) -> dict:
        headers = await app_headers()
        headers['Host'] = "apijs.ksapisrv.com"
        url, payload = await aweme_comment_path(photo_id=photo_id, pcursor=pcursor)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()


    async def aweme_sub_comment(self, photo_id, root_comment_id, pcursor) -> dict:
        headers = await app_headers()
        headers['Host'] = "apijs2.gifshow.com"
        url, payload = await aweme_sub_comment_path(photo_id=photo_id, root_comment_id=root_comment_id, pcursor=pcursor)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()


    async def user_post(self, user_id: str, pcursor:str, cookie:str):
        if not user_id or not cookie:
            raise CustomException()
        headers = await base_headers(cookie=cookie, referer=f"https://www.kuaishou.com/profile/{user_id}")
        data = await base_user_post(user_id, pcursor)
        response = await self._http_request(url=self.base_url, headers=headers, allow_redirects=True, json=data,
                                            proxy=await self._proxy(), request_method="POST")
        return response.json()

    async def user_info(self, user_id: str, cookie:str):
        if not user_id or not cookie:
            raise CustomException()
        headers = await base_headers(cookie=cookie, referer=f"https://www.kuaishou.com/profile/{user_id}")
        data = await base_user_info(user_id)
        response = await self._http_request(url=self.base_url, headers=headers, allow_redirects=True, json=data,
                                            proxy=await self._proxy(), request_method="POST")
        return response.json()




    async def user_post_v3(self, share_text: str):
        share_text = await self._extract_url(share_text)
        headers = await aweme_detail_headers()
        response = await self._http_request(url=share_text, headers=headers, allow_redirects=True,
                                            proxy=await self._proxy())
        match = re.search(r'window.INIT_STATE =(.*?)</script>', response.text, re.DOTALL)
        if match:
            data = match.group(1)
            extracted_data = self._extract_keys(json.loads(data))
            return extracted_data
        return None


    async def user_post_app(self, user_id:str, pcursor:str):
        headers = await app_headers()
        headers['Host'] = "apijs2.ksapisrv.com"
        url, payload = await user_post_app_path(app=self.request.app, user_id=user_id, pcursor=pcursor)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()

    async def user_info_v2(self, share_text: str):
        share_text = await self._extract_url(share_text)
        headers = await aweme_detail_headers()
        response = await self._http_request(url=share_text, headers=headers, allow_redirects=True,
                                            proxy=await self._proxy())
        response_url = str(response.url)
        parsed_url = urlparse(response_url)
        query_params = parse_qs(parsed_url.query)
        fid = query_params.get("fid", None)
        r_text = r'<script>window\.INIT_STATE = (.*?)</script>'
        match = re.search(r_text, response.text, re.DOTALL)
        try:
            wid_value = match.group(1)
            res = json.loads(wid_value)
            result = await self.find_user_profiles(res)
            filter_data = await self.remove_dict_with_fid(result, fid[0])
            return filter_data
        except Exception as e:
            raise CustomException(message=f"获取信息失败，请检查URL链接 {e}")


    async def user_info_v3(self, user_id:str):
        headers = await app_headers()
        headers['Host'] = "apijs2.ksapisrv.com"
        url, payload = await user_info_v3_path(self.request.app, user_id=user_id)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()


    async def search_aweme(self, keyword, pcursor, cookie):

        if not keyword or not cookie:
            raise CustomException()
        headers = await base_headers(cookie=cookie, referer=f"https://www.kuaishou.com/")
        data = await search_video_data(keyword=keyword, pcursor=pcursor)
        response = await self._http_request(url=self.base_url, headers=headers, allow_redirects=True, json=data,
                                            proxy=await self._proxy(), request_method="POST")
        return response.json()

    async def short_link(self, photo_id):
        headers = await app_headers()
        headers['Host'] = "api.kuaishouzt.com"
        url, payload = await short_link_path(self.request.app,photo_id=photo_id)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()


    async def user_short_link(self, user_id):
        headers = await app_headers()
        headers['Host'] = "api.kuaishouzt.com"
        url, payload = await user_short_link_path(app=self.request.app, user_id=user_id)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()



    async def hot_billboard(self):
        headers = await base_headers(cookie="",referer=f"https://www.kuaishou.com/?isHome=1")
        response = await self._http_request(url=home_url, headers=headers, allow_redirects=True,
                                            proxy=await self._proxy())
        item = self.extract_vision_hot_rank_items(response.text)
        return item


    async def hot_billboard_v2(self, board_type):
        headers = await app_headers()
        headers['Host'] = "apijs1.gifshow.com"
        url, payload = await hot_billboard_v2_path(board_type=board_type)
        sig_payload = await self.sig_data(url=url, payload=payload)
        response = await self._http_request(url=url, headers=headers, data=sig_payload, allow_redirects=True,
                                            proxy=await self._proxy(), request_method='POST')
        return response.json()

