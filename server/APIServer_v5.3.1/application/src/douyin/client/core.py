#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：core.py
@IDE     ：PyCharm 

@Date    ：2025/4/15 21:49 
'''
import asyncio
import base64
import json
import random
import re
import time
import uuid
import urllib.parse
from typing import Optional, Union

import httpx
from curl_cffi import requests

from application.src.douyin.args.abogus_old import encrypt_abogus
from application.src.douyin.args.common import generate_ttwid, extract_json_from_string, get__ac_signature, \
    get_douyin_cookies, generate_ttwid_so, process_data_in_js
from application.src.douyin.client.base import DouyinClient
from application.src.douyin.client.parameter import aweme_detail_path, mulptile_aweme_detail_path, aweme_detail_v4_path, \
    user_data_path, user_data_v2_path, user_data_v4_path, IME_HEADERS, user_detail_by_u_id, user_post_path, \
    user_post_v2_path, user_mix_path, mix_info_path, mix_aweme_list_path, search_user_aweme_path, user_fav_path, \
    aweme_root_comment_path, aweme_sub_comment_path, user_series_list_path, series_info_path, series_aweme_list_path, \
    general_search_v2_path, search_aweme_path, X_PC_UA, search_user_v2_path, search_music_path, music_path, \
    music_aweme_path, search_hash_tag_path, search_challenge_path, hash_tag_info_path, hash_tag_aweme_path, \
    hash_tag_aweme_path_v2, general_search_path, search_aweme_v2_path, search_live_path, live_room_path, \
    check_user_live_path, live_user_path, aweme_danmaku_path, short_link_path, aweme_qr_code_path, search_sug_path, \
    hot_spot_aladdin_path, share_to_scheme_path, APP_HEADERS, nearby_aweme_path, get_live_room_by_map_path, \
    stream_search_path, ANY_ACCOUNT_HEADERS, medium_channel_feed_path, aweme_board_path, aweme_shorten_path, \
    stream_search_path_app, params_v2_path, search_params_path, search_stream_path, week_select_path, \
    search_challenge_path_v2, search_user_v3_path, user_post_path_v2, general_search_v3_path, search_aweme_v3_path, \
    index_feed_path
from application.src.douyin.client.search import Search, get_cookie
from core import CustomException
from core.permit.licenses import get_general_search
from core.permit.sdmain import search_main
from libs import get_request_proxy
from libs.common import splitParams, generate_random_string_alph, generate_random_string, quote_keyword, extract_url


class Client(DouyinClient):

    async def aweme_detail(self, aweme_id: str, cookie: Optional[str] = None, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await aweme_detail_path(aweme_id=aweme_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def aweme_detail_v3(self, aweme_id: str, proxy: Optional[str] = None) -> dict:
        url = f"https://www.iesdouyin.com/share/video/{aweme_id}"
        headers = await self._mobile_header()
        response = await self._http_request(url=url, headers=headers)
        if response.status_code == 200:
            res = await self.parse_aweme_detail_html(response.text)
            return res
        raise CustomException(message="视频详情解析失败")

    async def aweme_detail_v4(self, aweme_id: str, cookie: Optional[str] = None, proxy: Optional[str] = None) -> dict:
        url = f"{self.pc_domain}/aweme/v1/web/aweme/detail/?"
        params = await aweme_detail_v4_path(aweme_id=aweme_id)
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def user_detail(self, sec_user_id: str, cookie: Optional[str] = None, proxy: Optional[str] = None) -> dict:
        url = f"{self.pc_domain}/aweme/v1/web/user/profile/other/?"
        params = await user_data_path(sec_user_id=sec_user_id)
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def user_detail_v2(self, sec_user_id: str, cookie: Optional[str] = None, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_data_v2_path(sec_user_id=sec_user_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=await self._app_cookie(
            device_data=device_data) if not cookie else cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_detail_v3(self, sec_user_id: str, proxy: Optional[str] = None) -> dict:
        url = f"https://www.amemv.com/web/api/v2/user/info/?sec_uid={sec_user_id}"
        headers = await self._pc_header()
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_detail_v4(self, sec_user_id: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        awemeim_guid = f"00862fd1a20f9e{await generate_random_string_alph(18)}"
        url = await user_data_v4_path(sec_user_id=sec_user_id, did=device_data['device_id_str'],
                                      iid=device_data['install_id_str'],
                                      awemeim_guid=awemeim_guid)
        headers = IME_HEADERS.copy()
        headers.update({
            "Cookie": f"passport_csrf_token={await generate_random_string()}; uid_tt_ss={await generate_random_string()}"})
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_detail_by_uid(self, user_id: str, cookie: Optional[str] = None, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_detail_by_u_id(user_id=user_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=await self._app_cookie(
            device_data=device_data) if not cookie else cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_detail_by_short_id(self, user_id: str, cookie: str, proxy: Optional[str] = None) -> dict:
        url = f"https://www.amemv.com/web/api/v2/user/info/?unique_id={user_id}"
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_post(self, sec_user_id: str, max_cursor: str = "", count: str = "12", filter_type: str = "",
                        cookie: str = "", proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_post_path(sec_user_id=sec_user_id, max_cursor=max_cursor, count=count, filter_type=filter_type, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str,
                                         cookies=cookie if cookie else await self._app_cookie(device_data=device_data))
        response = await self._http_request(url=url, headers=headers, request_method="POST")
        return response.json()

    async def user_post_v2(self, sec_user_id: str, user_id: str, max_cursor: str = "", count: str = "12"):
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_post_path_v2(sec_user_id=sec_user_id, max_cursor=max_cursor, count=count, user_id=user_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=await self._app_cookie(device_data=device_data))
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_new_post(self, sec_user_id: str, count: str, max_cursor: str = "", cookie: str = "",
                            proxy: Optional[str] = None) -> dict:
        url = f"{self.pc_domain}/aweme/v1/web/aweme/post/?"
        params = await user_post_v2_path(sec_user_id=sec_user_id, count=count, max_cursor=max_cursor)
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def user_mix(self, sec_user_id: str, cursor: str = "", count: str = "12",
                       proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_mix_path(sec_user_id=sec_user_id, cursor=cursor, count=count, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def mix_info(self, mix_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await mix_info_path(mix_id=mix_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def mix_aweme_list(self, mix_id, count, cursor, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await mix_aweme_list_path(mix_id=mix_id, count=count, cursor=cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def search_user_aweme(self, uid: str, keyword: str, count: str, cursor: str, search_id: str, cookie: str = "",
                                proxy: Optional[str] = None) -> dict:
        keyword = quote_keyword(keyword=keyword)
        url = f"{self.pc_domain}/aweme/v1/web/home/search/item/?"
        params = await search_user_aweme_path(user_uid=uid, keyword=keyword, offset=cursor, count=count,
                                              search_id=search_id)
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def user_fav(self, sec_user_id: str, count: str, max_cursor: str, cookie: str,
                       proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_fav_path(sec_user_id=sec_user_id, count=count, max_cursor=max_cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str,
                                         cookies=cookie if cookie else await self._app_cookie(device_data=device_data))
        response = await self._http_request(url=url, headers=headers, request_method='POST')
        return response.json()

    async def aweme_root_comments(self, aweme_id: str, count: str, cursor: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await aweme_root_comment_path(aweme_id=aweme_id, count=count, cursor=cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def aweme_sub_comments(self, aweme_id: str, comment_id: str, count: str, cursor: str,
                                 proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await aweme_sub_comment_path(aweme_id=aweme_id, comment_id=comment_id, count=count, cursor=cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def user_series_list(self, sec_user_id: str, count: str, cursor: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await user_series_list_path(sec_user_id=sec_user_id, count=count, cursor=cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def series_info(self, series_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await series_info_path(series_id=series_id, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def series_aweme_list(self, series_id, count, cursor, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        url = f"{self.app_domain}{await series_aweme_list_path(series_id=series_id, count=count, cursor=cursor, device_data=device_data)}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def general_search_stream_app(self, keyword: str, count="12", cookie: str = ""):
        path, data = await stream_search_path_app(keyword, count)

        url = f"https://tsearch.amemv.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        return response.text

    async def general_search(self, keyword: str, publish_time: str, content_type: str, sort_type: str,
                             filter_duration: str,
                             offset: str, count: str, search_id: str, cookie: str,
                             proxy: Optional[str] = None) -> dict:
        result = await get_general_search(keyword=keyword, publish_time=publish_time, content_type=content_type,
                                          sort_type=sort_type, filter_duration=filter_duration, offset=offset,
                                          count=count)
        return result

    async def general_search_stream(self, keyword: str, cookie: str = "",
                                    proxy: Optional[str] = None):
        path, headers = await stream_search_path(keyword=keyword)
        url = f"https://www.douyin.com/aweme/v1/web/general/search/stream/?{path}"
        response = await self._http_request(url=url, headers=headers)
        return response.text

    async def general_search_v2(self, keyword: str, publish_time: str, content_type: str, sort_type: str,
                                filter_duration: str, search_range: str,
                                offset: str, count: str, search_id: str, cookie: str,
                                proxy: Optional[str] = None, ua: Optional[str] = None) -> dict:
        proxy = await get_request_proxy(self.request)

        url, params = await general_search_v2_path(
            keyword=keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
            filter_duration=filter_duration,
            content_type=content_type,
            search_range=search_range,
            search_id=search_id
        )

        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        headers = {
            "User-Agent": UA,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.douyin.com/search/",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        cookie = cookie if cookie else await get_cookie(headers, proxy=proxy)
        headers['cookie'] = cookie
        a_bogus = await process_data_in_js(url=urllib.parse.urlencode(params), userAgent=UA)
        params.update({
            "a_bogus": "Qv4fhe6iOZmVKdKS8CBtt-IUeAo/rP8yWBTKb91P7OzeO70aE8PMBOatbxz-LtWjlRBkwo/78fslTfVb0GX0ZorkomZfS20yG4AVIXfo8qivGFXQDNfZCwvqSJtYWmkE8QoyJlUlAtma2dK4LpazUd5yyApi4mvpQrabdcUaY9evg0s9BHqouPtDPwzKUyAv"
        })

        response = await self._http_request(url=url, params=params, headers=headers)
        return response.json()

    async def general_search_v3(self, keyword: str, publish_time: str, content_type: str, sort_type: str,
                                filter_duration: str, search_range: str,
                                offset: str, count: str, search_id: str, cookie: str,
                                proxy: Optional[str] = None, ua: Optional[str] = None) -> dict:
        url, params = await general_search_v3_path(
            keyword=keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
            filter_duration=filter_duration,
            content_type=content_type,
            search_range=search_range,
            search_id=search_id
        )
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) douyin/5.7.2 Chrome/108.0.5359.215 Electron/22.3.18-tt.9.release.main.68 TTElectron/22.3.18-tt.9.release.main.68 Safari/537.36 awemePcClient/5.7.2 buildId/12307271 osName/Mas"
        # a_bogus = await encrypt_abogus(user_agent=ua, query=urllib.parse.urlencode(params), body="")
        # params.update({
        #     "a_bogus": a_bogus
        # })
        cookie = cookie if cookie else f"ttwid={await generate_ttwid(self.request)}"
        headers = {
            "User-Agent": ua,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN",
            "referer": "https://www.douyin.com/jingxuan/search/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-aweme-clientversion": "5.7.2",
            "x-aweme-devicemanufacturer": "Apple Inc.",
            "x-aweme-devicemodel": "Mac1512",
            "x-aweme-deviceos": "Mac OS X 15.2.0",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "cookie": cookie,
        }
        response = await self._http_request(url=url, params=params, headers=headers)
        return response.json()

    async def any_account(self, proxy: Optional[str] = None) -> dict:
        proxy = await get_request_proxy(self.request)
        cookie = await get_douyin_cookies(proxy=proxy)
        return cookie

    async def search_aweme(self, keyword: str, sort_type: str, publish_time: str,
                           filter_duration: str, search_range: str, offset: str, count: str, search_id: str,
                           cookie: Optional[str] = None,
                           proxy: Optional[str] = None, ua: Optional[str] = None) -> dict:
        proxy = await get_request_proxy(self.request)

        url, params = await search_aweme_path(
            keyword=keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
            filter_duration=filter_duration,
            search_range=search_range,
            search_id=search_id
        )
        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        headers = {
            "User-Agent": UA,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.douyin.com/search/",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        cookie = cookie if cookie else await get_cookie(headers, proxy=proxy)
        headers['cookie'] = cookie

        a_bogus = await process_data_in_js(url=urllib.parse.urlencode(params), userAgent=UA)
        params.update({
            "a_bogus": a_bogus
        })

        response = await self._http_request(url=url, params=params, headers=headers)
        return response.json()

    async def search_aweme_v2(self, keyword: str, sort_type: str, publish_time: str,
                              filter_duration: str, offset: str, count: str, search_id: str, cookie: str, search_d:str=None,
                              proxy: Optional[str] = None) -> dict:
        proxy = await get_request_proxy(self.request)
        if not search_d or search_d == "":
            device_data = await search_main(proxy=proxy)
            search_d = base64.b64encode(json.dumps(device_data).encode('utf-8')).decode("utf-8")
        else:
            device_data = json.loads(base64.b64decode(search_d).decode("utf-8"))
        path, data = await search_aweme_v2_path(keyword, count, offset, sort_type, publish_time, filter_duration,
                                                device_data, search_id=search_id)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        result = response.json()
        result['search_d'] = search_d
        return result

    async def search_user_v2(self, keyword: str, user_type: str, user_fans: str,
                             offset: str, count: str, search_id: str, cookie: str,
                             proxy: Optional[str] = None, ua: Optional[str] = None) -> dict:
        url, params = await search_user_v2_path(
            keyword=keyword,
            count=count,
            offset=offset,
            douyin_user_fans=user_fans,
            douyin_user_type=user_type,
            search_id=search_id
        )
        keyword = quote_keyword(keyword)
        ua = ua or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"

        headers = {
            "User-Agent": ua,
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": f"https://www.douyin.com/jingxuan/search/{keyword}?type=user",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        # a_bogus = await encrypt_abogus(user_agent=ua, query=urllib.parse.urlencode(params), body="")
        # params.update({
        #     "a_bogus": a_bogus
        # })
        proxy = await get_request_proxy(self.request)
        if not cookie:
            cookie = await get_douyin_cookies(proxy=proxy)
        headers['cookie'] = cookie
        response = await self._http_request(url=url, params=params, headers=headers)
        result = response.json()

        result['cookie'] = cookie
        return result

    async def search_aweme_v3(self, keyword: str, publish_time: str, sort_type: str,
                              filter_duration: str, search_range: str,
                              offset: str, count: str, search_id: str, cookie: str,
                              proxy: Optional[str] = None, ua: Optional[str] = None) -> dict:
        url, params = await search_aweme_v3_path(
            keyword=keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
            filter_duration=filter_duration,
            search_range=search_range,
            search_id=search_id
        )
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) douyin/5.7.2 Chrome/108.0.5359.215 Electron/22.3.18-tt.9.release.main.68 TTElectron/22.3.18-tt.9.release.main.68 Safari/537.36 awemePcClient/5.7.2 buildId/12307271 osName/Mas"
        # a_bogus = await encrypt_abogus(user_agent=ua, query=urllib.parse.urlencode(params), body="")
        # params.update({
        #     "a_bogus": a_bogus
        # })
        cookie = cookie if cookie else f"ttwid={await generate_ttwid(self.request)}"
        headers = {
            "User-Agent": ua,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN",
            "referer": "https://www.douyin.com/jingxuan/search/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-aweme-clientversion": "5.7.2",
            "x-aweme-devicemanufacturer": "Apple Inc.",
            "x-aweme-devicemodel": "Mac1512",
            "x-aweme-deviceos": "Mac OS X 15.2.0",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "cookie": cookie,
        }
        response = await self._http_request(url=url, params=params, headers=headers)
        return response.json()

    async def search_user_v3(self, keyword: str, douyin_user_type: str, douyin_user_fans: str,
                             offset: str, count: str, search_id: str, cookie: str,search_d:str=None,
                             proxy: Optional[str] = None) -> dict:
        proxy = await get_request_proxy(self.request)
        if not search_d or search_d == "":
            device_data = await search_main(proxy=proxy)
            search_d = base64.b64encode(json.dumps(device_data).encode('utf-8')).decode("utf-8")
        else:
            device_data = json.loads(base64.b64decode(search_d).decode("utf-8"))
        path, data = await search_user_v3_path(keyword=keyword, count=count, offset=offset,
                                               douyin_user_fans=douyin_user_fans, douyin_user_type=douyin_user_type,
                                               device_data=device_data, search_id=search_id)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        result = response.json()
        result['search_d'] = search_d
        return result

    async def get_cookie(self, headers, proxy):
        async with requests.AsyncSession(proxy=proxy) as session:
            response = await session.get('https://www.douyin.com/', headers=headers)
            cookies_n = session.cookies.get_dict()
            signature = get__ac_signature(
                int(time.time()),
                'www.douyin.com/',
                cookies_n['__ac_nonce'],
                headers['User-Agent']
            )
            session.cookies.set('__ac_signature', signature)
            await session.get('https://www.douyin.com/', headers=headers)
            cookie = "; ".join([f"{k}={v}" for k, v in session.cookies.items()])
            return cookie

    async def search_stream(self, keyword: str, content_type: str, filter_duration: str, sort_type: str,
                            publish_time: str, search_id: str, count: str, offset: str, search_range: str, cookie: str):

        proxy = await get_request_proxy(self.request)

        url, params = await search_stream_path(
            keyword=keyword,
            count=count,
            offset=offset,
            sort_type=sort_type,
            publish_time=publish_time,
            filter_duration=filter_duration,
            content_type=content_type,
        )

        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        headers = {
            "User-Agent": UA,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.douyin.com/search/",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        cookie = cookie if cookie else await get_cookie(headers, proxy=proxy)
        headers['cookie'] = cookie

        a_bogus = await process_data_in_js(url=urllib.parse.urlencode(params), userAgent=UA)
        params.update({
            "a_bogus": a_bogus
        })

        response = await self._http_request(url=url, params=params, headers=headers)
        for line in response.text.splitlines():
            line = line.strip()
            # 跳过 chunked 长度行、空行
            if not line or re.fullmatch(r'[0-9a-fA-F]+', line):
                continue

            try:
                obj = json.loads(line)  # 此时是 dict
            except json.JSONDecodeError:
                continue  # 不是 JSON 就跳过

            # 你要的条件
            if isinstance(obj, dict) and len(obj.get("data", [])) >= 2:
                return obj
                # 或者 print(obj)  # 已转好的字典
        return None

    async def search_note(self, keyword: str, search_id: Union[None, str], search_session_id: Union[None, str],
                          count: str, cursor: str, cookie: str):
        device_data = await self._get_device_data()

        url = f"{self.search_domain}/aweme/v1/search/experience/"
        params = await search_params_path(keyword=keyword, cursor=cursor, count=count, search_id=search_id,
                                          search_session_id=search_session_id)
        url, headers = await self._search_encrypt_data(url=url, params=params, device_data=device_data)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def search_music(self, keyword: str, count: str, cursor: str, search_id: Union[None, str], ) -> dict:
        proxy = await get_request_proxy(self.request)
        device_data = await search_main(proxy=proxy)
        path, data = await search_music_path(keyword=keyword, cursor=cursor, count=count, search_id=search_id,
                                             device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        return response.json()

    async def music_info(self, music_id: str, cookie: str = '', proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path = await music_path(music_id=music_id, device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def music_aweme(self, music_id: str, cursor: str, count: str, cookie: str = "",
                          proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data(device_type="simple")
        path = await music_aweme_path(music_id=music_id, cursor=cursor, count=count, device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def search_hash_tag(self, keyword: str, count: str, page: str) -> dict:

        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/material/challenge_billboard"
        data = {"page": int(page), "page_size": int(count), "date_window": 168, "sub_type": 2001, "keyword": keyword,
                "tag_version": "v2"}
        response = await self._http_request(url=url, json=data, headers=headers, request_method="POST")
        return response.json()

    async def search_challenge(self, keyword: str, count: str, cursor: str, search_id: str) -> dict:
        device_data = await self._get_device_data(device_type="search")
        path, data = await search_challenge_path_v2(keyword=keyword, cursor=cursor, count=count,
                                                    device_data=device_data, search_id=search_id)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        return response.json()

    async def hash_tag_info(self, keyword: str, cookie: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path = await hash_tag_info_path(keyword=keyword, device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def hash_tag_aweme(self, ch_id: str, count: str, cursor: str, sort_type: str, cookie: str,
                             proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data(device_type="simple")
        path = await hash_tag_aweme_path(ch_id=ch_id, count=count, cursor=cursor, sort_type=sort_type,
                                         device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def hash_tag_aweme_v2(self, keyword: str, count: str, cursor: str, sort_type: str, cookie: str,
                                proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data(device_type="simple")
        path = await hash_tag_aweme_path_v2(keyword=keyword, count=count, cursor=cursor, sort_type=sort_type,
                                            device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def aweme_new_fans_count(self, aweme_id: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/item_analysis/{aweme_id}/data_trends/index"
        response = await self._http_request(url=url, headers=headers)
        new_fans_cnt = response.json().get("data").get("new_fans_cnt")
        res_data = {
            "new_fans_cnt": new_fans_cnt,
            "aweme_id": aweme_id
        }
        return res_data

    async def search_keyword_value(self, keyword: str, date_window: int, page_num: int, sub_type: int, page_size: int):
        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/dashboard/hot_search/query_list"
        data = {
            "page_num": int(page_num),
            "page_size": int(page_size),
            "date_window": int(date_window),
            "sub_type": int(sub_type),
            "keyword": keyword
        }
        response = await self._http_request(url=url, headers=headers, json=data, request_method="POST")
        return response.json()

    async def aweme_user_tag(self, sec_user_id: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/author_analysis/author_info?sec_uid={sec_user_id}"
        response = await self._http_request(url=url, headers=headers)
        result = response.json().get("data")
        del result['fans_milestone']
        return result

    async def user_product_data(self, sec_uid: str, day: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/author_analysis/product_analysis/product_data?sec_uid={sec_uid}&day={day}&msToken="
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def search_user(self, keyword: str, cursor: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data("billboard")
        headers = await self._pc_header(cookies=device_data)
        url = f"{self.request.app.ctx.BASE_BILLBOARD}/v1/monitor/author/query_user_v2?keyword={keyword}&cursor={cursor}"
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def search_live_user(self, keyword: str, offset: str, count: str, cookie: str, search_id: str,
                               proxy: Optional[str] = None) -> dict:
        url, params = await search_live_path(
            keyword=keyword,
            count=count,
            offset=offset,
            search_id=search_id
        )

        if not cookie:
            raise CustomException(message="需传入cookie")
        UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        headers = {
            "User-Agent": UA,
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.douyin.com/jingxuan/search/",
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": cookie
        }
        a_bogus = await process_data_in_js(url=urllib.parse.urlencode(params), userAgent=UA)
        params.update({
            "a_bogus": a_bogus
        })
        response = await self._http_request(url=url, params=params, headers=headers)
        return response.json()

    async def search_live_user_v2(self, keyword: str, cursor: str, count: str, cookie: str, search_id: Union[None, str],
                                  search_session_id: Union[None, str],
                                  proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()

        url = f"{self.search_domain}/aweme/v2/search/live/"
        params = await search_params_path(keyword=keyword, cursor=cursor, count=count, search_id=search_id,
                                          search_session_id=search_session_id)
        url, headers = await self._search_encrypt_data(url=url, params=params, device_data=device_data)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def live_room_info(self, web_rid: str, cookie: str, proxy: Optional[str] = None) -> dict:
        url = "https://live.douyin.com/webcast/room/web/enter/"
        params = {
            "aid": "6383",
            "app_name": "douyin_web",
            "live_id": "1",
            "device_platform": "web",
            "language": "zh-CN",
            "enter_from": "page_refresh",
            "cookie_enabled": "true",
            "screen_width": "2560",
            "screen_height": "1440",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Edge",
            "browser_version": "140.0.0.0",
            "web_rid": web_rid,
            "enter_source": "",
            "is_need_double_stream": "false",
            "insert_task_id": "",
            "live_reason": "",
            "msToken": "",
        }
        a_bogus = await encrypt_abogus(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            query=urllib.parse.urlencode(params), body="")
        params.update({
            "a_bogus": a_bogus
        })
        proxy = await get_request_proxy(self.request)
        cookie = await generate_ttwid(request=self.request)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": f"ttwid={cookie};",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://live.douyin.com/",
            "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

        with httpx.Client(http2=True, proxy=proxy) as client:
            res = client.get(url=url, params=params, headers=headers)
            result = res.json()

        return result

    async def live_room_info_by_id(self, room_id: str, proxy: Optional[str] = None) -> dict:
        url = f"https://webcast.amemv.com/douyin/webcast/reflow/{room_id}"
        headers = await self._pc_header()
        response = await self._http_request(url=url, headers=headers)
        result = await self.parse_live_info(response.text)
        if result:
            return result
        return None

    async def check_user_live_status(self, sec_user_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path, data = await check_user_live_path(sec_user_id=sec_user_id, device_data=device_data)
        url = f"https://webcast5-normal-lq.amemv.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, host="https://webcast5-normal-lq.amemv.com")
        response = await self._http_request(url=url, headers=headers, data=data, request_method="POST")
        return response.json()

    async def live_room_user_list(self, room_id: str, sort_type: str,cookie:str=None, proxy: Optional[str] = None) -> dict:
        url = f"https://live.douyin.com/webcast/ranklist/audience/?"
        params = await live_user_path(room_id=room_id, sort_type=sort_type)
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header(referer="https://live.douyin.com/", cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def aweme_danmaku(self, aweme_id, start_time, end_time, proxy: Optional[str] = None) -> dict:
        params = await aweme_danmaku_path(aweme_id=aweme_id, start_time=start_time, end_time=end_time)
        url = f"{self.pc_domain}/aweme/v1/web/danmaku/get_v2/?"
        params_with_ab = await self.process_a_bogus(params)
        headers = await self._pc_header()
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        return response.json()

    async def user_short_link(self, sec_user_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path, data = await short_link_path(sec_user_id=sec_user_id, device_data=device_data, is_video=False)
        url = f"https://lf.snssdk.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, host="https://lf.snssdk.com")
        response = await self._http_request(url=url, headers=headers, data=data, request_method='POST')
        return response.json()

    async def aweme_short_link(self, aweme_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path, data = await short_link_path(aweme_id=aweme_id, device_data=device_data)
        url = f"https://lf.snssdk.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, host="https://lf.snssdk.com")
        response = await self._http_request(url=url, headers=headers, data=data, request_method='POST')
        return response.json()

    async def aweme_qr_code(self, aweme_id, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path, data = await aweme_qr_code_path(device_data=device_data, aweme_id=aweme_id)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, data=data, headers=headers, request_method='POST')
        return response.json()

    async def search_sug(self, keyword: str, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path = await search_sug_path(keyword=keyword, device_data=device_data)
        url = f"https://search5-search-lq.amemv.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def hot_spot_aladdin(self, sentence_id, sort_type, cursor, proxy: Optional[str] = None) -> dict:
        device_data = await self._get_device_data()
        path = await hot_spot_aladdin_path(sentence_id=sentence_id, sort_type=sort_type, cursor=cursor,
                                           device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def get_scheme(self, share_text, proxy: Optional[str] = None) -> dict:

        short_url = await extract_url(share_text)
        headers = APP_HEADERS.copy()
        short_url = await self._http_request(url=short_url, headers=headers, allow_redirects=False)
        short_url = short_url.headers.get("location")
        device_data = await self._get_device_data()
        path = await share_to_scheme_path(url=str(short_url), device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def nearby_aweme(self, city_code, latitude, longitude, cookie=None, lock_data=None,
                           proxy: Optional[str] = None):
        if not lock_data:
            lock_device = False
            device_data = await self._get_device_data(device_type='simple')
        else:
            device_data = json.loads(await self.request.app.ctx.curl_client.decrypt_data(lock_data))
            lock_device = True
        path = await nearby_aweme_path(city_code, latitude, longitude, device_data, lock_device)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        cookie = cookie
        headers = await self._app_header(params_str, cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        result = response.json()
        result['lock_data'] = lock_data if lock_data else await self.request.app.ctx.curl_client.encrypt_data(
            device_data)
        return result

    async def live_room_by_map(self, city_code, max_time, did, iid, proxy: Optional[str] = None) -> dict:
        if not did and not iid:
            device_data = await self._get_device_data()
            did = device_data['device_id']
            iid = device_data['install_id']
        path = await get_live_room_by_map_path(city_code=city_code, max_time=max_time, did=did, iid=iid)
        url = f"https://webcast5-normal-lq.amemv.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, host="https://webcast5-normal-lq.amemv.com")
        response = await self._http_request(url=url, headers=headers)

        data = response.json()
        data['did'] = did
        data['iid'] = iid
        return data

    async def medium_channel_feed(self, tag_id, install_time, refresh_index, cookie):

        url = f"{self.pc_domain}/aweme/v1/web/module/feed/?"
        if not install_time or install_time == "":
            install_time = int(time.time())
        if not refresh_index or refresh_index == "":
            refresh_index = 1
        params = await medium_channel_feed_path(tag_id=tag_id, install_time=install_time, refresh_index=refresh_index)
        params_with_ab = await self.process_a_bogus_old(params=params)
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url + params_with_ab, headers=headers)
        result = response.json()
        result['cookie'] = headers['Cookie']
        result['install_time'] = install_time
        return result

    async def aweme_board(self, board_type, board_sub_type=""):
        device_data = await self._get_device_data(device_type='simple')
        path = await aweme_board_path(board_type=board_type, board_sub_type=board_sub_type, device_data=device_data)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        return response.json()

    async def multiple_aweme_detail(self, item_ids: str, proxy: Optional[str] = None) -> dict:
        try:
            if not item_ids or item_ids == "" or item_ids == "[]":
                raise CustomException(message="请传入有效的ID列表")
            item_list = json.loads(item_ids)
        except:
            raise CustomException(message="请传入有效的ID列表")
        device_data = await self._get_device_data("simple")
        url = f"{self.app_domain}{await mulptile_aweme_detail_path(device_data=device_data)}"
        data = {"aweme_ids": f"{item_list}", "origin_type": "", "push_params": "", "meta_params": "", "card_type": "",
                "request_source": "0", "from_push": "0", "item_level": "0"}
        headers = APP_HEADERS.copy()
        sign_data = {
            "url": url,
            "headers": headers,
            "data": data,
        }
        sign_response = await self.request.app.ctx.curl_client.aweme_encrypt_data(sign_data)
        response = await self._http_request(url=sign_response['data']['url'], headers=sign_response['data']['headers'],
                                            data=data, request_method="POST")
        return response.json()

    async def aweme_shorten(self, aweme_id, aweme_type):
        if not aweme_id:
            raise CustomException(message="请传入有效的ID")

        device_data = await self._get_device_data()
        path, data = await aweme_shorten_path(aweme_id=aweme_id, aweme_type=aweme_type, device_data=device_data)
        url = f"https://lf.snssdk.com{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str, host="https://lf.snssdk.com")
        response = await self._http_request(url=url, data=data, headers=headers, request_method="POST")
        return response.json()

    async def get_anonymous_cookie(self):
        search_url, search_params = await search_user_v2_path(keyword=str(range(1111, 9999)), count="10", offset="0",
                                                              douyin_user_type="", douyin_user_fans="", search_id="")
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        headers = {
            "User-Agent": ua,
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.douyin.com/",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        a_bogus = await encrypt_abogus(user_agent=ua, query=urllib.parse.urlencode(search_params), body="")
        search_params.update({
            "a_bogus": a_bogus
        })
        proxy = await get_request_proxy(self.request)
        cookie = await self.get_cookie(headers=headers, proxy=proxy)
        cookie += f";device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64;stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22;SEARCH_RESULT_LIST_TYPE=%22single%22;hevc_supported=true;IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22;volume_info=%7B%22isMute%22%3Atrue%2C%22isUserMute%22%3Atrue%2C%22volume%22%3A0.6%7D;x-web-secsdk-uid={str(uuid.uuid4())};WallpaperGuide=%7B%22showTime%22%3A{round(time.time() * 1000)}%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D"
        return cookie

    async def week_select_list(self, term="", next_page_ids=""):
        path = await week_select_path(term=term, next_page_ids=next_page_ids)
        url = f"{self.app_domain}{path}"
        params_str = splitParams(url)
        headers = await self._app_header(params_str)
        response = await self._http_request(url=url, headers=headers)
        data = response.json()
        return data

    async def index_feed(self, cookie: str, refresh_index: str):
        path = await index_feed_path(refresh_index=refresh_index)
        url = f"{self.pc_domain}{path}"
        headers = await self._pc_header(cookies=cookie)
        response = await self._http_request(url=url, headers=headers)
        result = response.json()
        if not cookie:
            result['cookie'] = headers['Cookie']
        return result
