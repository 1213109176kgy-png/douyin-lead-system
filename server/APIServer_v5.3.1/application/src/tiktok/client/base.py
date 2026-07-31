#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager
@File    ：base.py
@IDE     ：PyCharm

@Date    ：2025/4/22 11:22
'''
import json
import random
import re
import time
import urllib.parse

import httpx
from loguru import logger

from application.src.tiktok.args.xBogus import XBogus
from application.src.tiktok.args.x_g import Xgorgon
from application.src.tiktok.client.parameter import BASE_HEADERS, root_comment_url_path, app_headers, \
    sub_comment_url_path, user_post_path, general_search_path, search_user_path, search_item_path
from core import CustomException, json_success_response, get_device_data
from libs import get_request_proxy, get_request_data


class TikTokBase(object):
    def __init__(self, request):
        self.request = request

    async def get_proxy(self):
        return await get_request_proxy(self.request, proxy_type="overseas")
        # return None

    async def _get_id(self, share_text):

        link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          share_text.replace("#", ""))
        if not link:
            raise CustomException()
        url = link[0]
        headers = BASE_HEADERS.copy()
        response = await self.request.app.ctx.curl_client.http_get(url=url, proxy=await self.get_proxy(),
                                                                   headers=headers, requests_client="httpx")
        response_url = response.headers.get('Location') or url
        if "video" in response_url:
            match = re.search(r'/video/([^/?]+)', response_url)
        elif "note" in response_url:
            match = re.search(r'/note/([^/?]+)', response_url)
        elif "hashtag" in response_url:
            match = re.search(r'/hashtag/([^/?]+)', response_url)
        elif "challenge" in response_url:
            match = re.search(r'/challenge/([^/?]+)', response_url)
        elif "webcast.amemv.com/douyin/webcast/reflow/" in response_url:
            match = re.search(r'/douyin/webcast/reflow/([^/?]+)', response_url)
        elif "live.douyin.com" in response_url:
            match = re.search(r'live.douyin.com/([^/?]+)', response_url)
        else:
            match = re.search(r'/user/([^/?]+)', response_url)
        if match:
            id = match.group(1)
            return id
        else:
            raise CustomException(message="获取ID失败")

    async def __gen_ttwid(self, proxy=None) -> str:
        """
        生成请求必带的ttwid
        """
        request_cookie = ""
        retries = 0
        while retries < 3:
            try:
                headers = {
                    "cookie": request_cookie,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

                async with httpx.AsyncClient(proxy=proxy, timeout=60) as client:
                    response = await client.get(url="https://www.tiktok.com/explore", headers=headers)
                    cookie = response.cookies.get("ttwid", None)
                    if request_cookie:
                        request_cookie = f"ttwid={cookie}"
                    match = re.search(r'"wid":"(\d+)"', response.text)
                    odinId = re.search(r'"odinId":"(\d+)"', response.text)
                    wid_value = match.group(1)
                    odinId_value = odinId.group(1)
                    device_id = wid_value
                    data = {
                        "ttwid": response.cookies.get("ttwid"),
                        "device_id": device_id,
                        "odinId": odinId_value
                    }
                    self.request.app.ctx.tiktok_device_ttwid.append(data)

                    logger.info(f"GET TikTok Device Success")
                return data
            except Exception as e:
                logger.error(f"TikTok Device Error:{e}")
                retries += 1
                continue
        else:
            logger.error(f"TikTok Device Error")
            return None

    def get_ms_token(self, randomlength=107):
        base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789='
        return ''.join(random.choice(base_str) for _ in range(randomlength))

    async def __base_pc_headers(self, proxy, token_type=None):
        gen = await self.__gen_ttwid(proxy)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "referer": "https://www.tiktok.com/"
        }
        headers.update({"cookie": "msToken=" + self.request.app.ctx.tiktok_ms_token if hasattr(self.request.app.ctx,
                                                                                               'tiktok_ms_token') else "msToken=QyDGRslLyopyPl4G-kom6_Qi-Q0Vdr8_WzbRg7rN_RR-nTdUyQV6KueJI3hJrw_M3H1qEfMvPbJNHMObDawFqyoqC7FGwQiyFCGlfBPgNUX_aTpJklEgXrKNQO5g4cC0rApt68X3EskDqaAKYgxk_aU="})
        if token_type == "search_user":
            headers.update({"cookie": "msToken=" + self.request.app.ctx.tiktok_search_user_ms_token if hasattr(
                self.request.app.ctx,
                'tiktok_search_user_ms_token') else "msToken=QyDGRslLyopyPl4G-kom6_Qi-Q0Vdr8_WzbRg7rN_RR-nTdUyQV6KueJI3hJrw_M3H1qEfMvPbJNHMObDawFqyoqC7FGwQiyFCGlfBPgNUX_aTpJklEgXrKNQO5g4cC0rApt68X3EskDqaAKYgxk_aU="})
        if token_type == "general_search":
            headers.update({"cookie": "msToken=" + self.request.app.ctx.tiktok_general_search_ms_token if hasattr(
                self.request.app.ctx,
                'tiktok_general_search_ms_token') else "msToken=QyDGRslLyopyPl4G-kom6_Qi-Q0Vdr8_WzbRg7rN_RR-nTdUyQV6KueJI3hJrw_M3H1qEfMvPbJNHMObDawFqyoqC7FGwQiyFCGlfBPgNUX_aTpJklEgXrKNQO5g4cC0rApt68X3EskDqaAKYgxk_aU="})
        if token_type == "search_item":
            headers.update({"cookie": "msToken=" + self.request.app.ctx.tiktok_search_item_ms_token if hasattr(
                self.request.app.ctx,
                'tiktok_search_item_ms_token') else "msToken=QyDGRslLyopyPl4G-kom6_Qi-Q0Vdr8_WzbRg7rN_RR-nTdUyQV6KueJI3hJrw_M3H1qEfMvPbJNHMObDawFqyoqC7FGwQiyFCGlfBPgNUX_aTpJklEgXrKNQO5g4cC0rApt68X3EskDqaAKYgxk_aU="})

        headers['cookie'] = headers['cookie'] + ";ttwid=" + gen['ttwid']

        return headers, gen

    async def aweme_detail(self, request):
        data = await get_request_data(request)
        aweme_id = data.get("aweme_id", None)
        share_text = data.get("share_text", None)

        if not aweme_id:
            if not share_text:
                raise CustomException()
            aweme_id = await self._get_id(share_text) if await self._get_id(share_text) else None
            if not aweme_id:
                raise CustomException(message="请传入视频ID")
        url = f"https://www.tiktok.com/@orphic__sm_/video/{aweme_id}"
        headers = BASE_HEADERS.copy()
        response = await self.request.app.ctx.curl_client.http_get(url, headers=headers, proxy=await self.get_proxy(),
                                                                   requests_client="httpx")
        if not response:
            raise CustomException(message="获取视频详情失败，请重试")
        pattern = r'id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'  # 匹配所有的 HTML 标签
        script_list = re.findall(pattern, response.text)
        data = json.loads(script_list[0])
        aweme_info = data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']
        return json_success_response(data=aweme_info)

    async def user_detail(self, request):
        data = await get_request_data(request)
        sec_uid = data.get("sec_uid", None)
        unique_id = data.get("unique_id", None)

        if not unique_id and not sec_uid:
            raise CustomException(message="请传入sec_uid或unique_id")
        url = f"https://www.tiktok.com/@{sec_uid or unique_id}"
        headers = BASE_HEADERS.copy()
        response = await self.request.app.ctx.curl_client.http_get(url, headers=headers, proxy=await self.get_proxy(),
                                                                   requests_client="httpx")
        if not response:
            raise CustomException(message="获取用户详情失败，请重试")
        pattern = r'id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'  # 匹配所有的 HTML 标签
        script_list = re.findall(pattern, response.text)
        data = json.loads(script_list[0])
        aweme_info = data['__DEFAULT_SCOPE__']['webapp.user-detail']
        return json_success_response(data=aweme_info)

    async def aweme_root_comments(self, request):
        data = await get_request_data(request)
        aweme_id = data.get("aweme_id", None)
        cursor = data.get("cursor", "20")
        region = data.get("region", "JP")
        proxy = data.get('proxy')
        if not aweme_id:
            return CustomException(message="参数缺失")

        url = f"https://www.tiktok.com/api/comment/list/?"
        query = f"aid=1988&app_name=tiktok_web&aweme_id={aweme_id}&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F125.0.0.0%20Safari%2F537.36%20Edg%2F125.0.0.0&channel=tiktok_web&cookie_enabled=true&count=20&current_region={region}&cursor={cursor}&device_id=737200856270{str(random.randint(2222222, 9999999))}&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=4&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&os=windows&priority_region={region}&region={region}&screen_height=1080&screen_width=1920&tz_name=Asia%2FShanghai"
        x_b = XBogus()
        x_params = x_b.getXBogus(query)[0]
        url = url + x_params
        req_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Cookie": ""
        }
        req_headers.update({"cookie": "msToken=" + self.request.ctx.tiktok_ms_token if hasattr(self.request.ctx,
                                                                                               'tiktok_ms_token') else "msToken=QyDGRslLyopyPl4G-kom6_Qi-Q0Vdr8_WzbRg7rN_RR-nTdUyQV6KueJI3hJrw_M3H1qEfMvPbJNHMObDawFqyoqC7FGwQiyFCGlfBPgNUX_aTpJklEgXrKNQO5g4cC0rApt68X3EskDqaAKYgxk_aU="})

        res = await self.request.app.ctx.curl_client.http_get(url, headers=req_headers, proxy=await self.get_proxy(),
                                                              requests_client="httpx")
        if not res:
            return CustomException(message="获取失败")
        return json_success_response(res.json())

    async def aweme_sub_comment(self, request):
        data = await get_request_data(request)
        aweme_id = data.get("aweme_id", None)
        comment_id = data.get("comment_id", None)
        cursor = data.get("cursor", None)
        if not aweme_id:
            raise CustomException(message="请传入视频ID")
        if not comment_id:
            raise CustomException(message="请传入视频comment_id")

        url = f"https://api16-normal-useast5.tiktokv.us/aweme/v1/comment/list/reply/?"
        device_data = await get_device_data(request.app)
        params = await sub_comment_url_path(aweme_id=aweme_id, comment_id=comment_id, cursor=cursor,
                                            device_data=device_data)
        signature = Xgorgon(url=url + params, data=None, cookie=None)
        signature = signature.calc_gorg()
        headers = await app_headers(signature)
        response = await self.request.app.ctx.curl_client.http_get(url + params, headers=headers,
                                                                   proxy=await self.get_proxy(),
                                                                   requests_client="httpx")
        return json_success_response(data=response.json())

    async def user_post(self, request):
        data = await get_request_data(request)
        sec_uid = data.get("sec_uid", None)
        post_type = data.get("post_type", "0")
        count = data.get("count", "20")
        cursor = data.get("cursor", None)
        cookie = data.get("cookie", None)
        proxy = await self.get_proxy()
        if not sec_uid:
            raise CustomException("请传入sec_uid")

        # headers, gen = await self.__base_pc_headers(proxy)
        # if cookie:
        #     headers['cookie'] = cookie
        url = f"https://www.tiktok.com/api/post/item_list/"
        # query = await user_post_path(sec_uid=sec_uid, post_type=post_type, cursor=cursor, count=count, gen=gen)
        # x_b = XBogus()
        # x_params = x_b.getXBogus(query)[0]
        # url = url + x_params
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.tiktok.com/@shigeshow",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        params = {
            "WebIdLastTime": "0",
            "aid": "1988",
            "app_language": "zh-Hans",
            "app_name": "tiktok_web",
            "browser_language": "zh-CN",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
            "channel": "tiktok_web",
            "clientABVersions": "73675307",
            "cookie_enabled": "true",
            "count": "16",
            "coverFormat": "2",
            "cursor": cursor,
            "data_collection_enabled": "false",
            "device_platform": "web_pc",
            "enable_cache": "false",
            "focus_state": "false",
            "from_page": "user",
            "history_len": "14",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "language": "zh-Hans",
            "needPinnedItemIds": "true",
            "os": "windows",
            "post_item_list_request_type": "0",
            "priority_region": "",
            "referer": "",
            "region": "TW",
            "screen_height": "1440",
            "screen_width": "2560",
            "secUid": sec_uid,
            "tz_name": "Asia/Shanghai",
            "user_is_login": "false",
            "video_encoding": "mp4",
            "webcast_language": "zh-Hans"
        }

        res = await self.request.app.ctx.curl_client.http_get(url, params=params, headers=headers, proxy=proxy,
                                                              requests_client="httpx")
        # self.request.app.ctx.tiktok_ms_token = f"{res.cookies.get('msToken')}"
        return json_success_response(res.json())

    async def general_search(self, request):
        data = await get_request_data(request)
        keyword = data.get("keyword", None)
        cursor = data.get("cursor", "")
        search_id = data.get("search_id", "")
        cookie = data.get("cookie", None)
        proxy = await self.get_proxy()

        headers, gen = await self.__base_pc_headers(proxy, token_type="general_search")
        if cookie:
            headers['cookie'] = cookie
        url = f"https://www.tiktok.com/api/search/general/full/?"
        query = await general_search_path(keyword=keyword, cursor=cursor, search_id=search_id, gen=gen)
        x_b = XBogus()
        x_params = x_b.getXBogus(query)[0]
        url = url + x_params

        res = await self.request.app.ctx.curl_client.http_get(url, headers=headers, proxy=proxy,
                                                              requests_client="httpx")
        self.request.app.ctx.tiktok_general_search_ms_token = f"{res.cookies.get('msToken')}"
        return json_success_response(res.json())

    async def search_user(self, request):
        data = await get_request_data(request)
        keyword = data.get("keyword", None)
        cursor = data.get("cursor", "")
        search_id = data.get("search_id", "")
        cookie = data.get("cookie", None)
        proxy = await self.get_proxy()

        headers, gen = await self.__base_pc_headers(proxy, token_type="search_user")
        if cookie:
            headers['cookie'] = cookie
        url = f"https://www.tiktok.com/api/search/user/full/?"
        query = await search_user_path(keyword=keyword, cursor=cursor, search_id=search_id, gen=gen)
        x_b = XBogus()
        x_params = x_b.getXBogus(query)[0]
        url = url + x_params
        res = await self.request.app.ctx.curl_client.http_get(url, headers=headers, proxy=proxy,
                                                              requests_client="httpx")
        self.request.app.ctx.tiktok_search_user_ms_token = f"{res.cookies.get('msToken')}"
        return json_success_response(res.json())

    async def search_item(self, request):
        data = await get_request_data(request)
        keyword = data.get("keyword", None)
        cursor = data.get("cursor", "")
        search_id = data.get("search_id", "")
        cookie = data.get("cookie", None)
        proxy = await self.get_proxy()

        headers, gen = await self.__base_pc_headers(proxy, token_type="search_item")
        if cookie:
            headers['cookie'] = cookie
        url = f"https://www.tiktok.com/api/search/item/full/?"
        query = await search_item_path(keyword=keyword, cursor=cursor, search_id=search_id, gen=gen)
        x_b = XBogus()
        x_params = x_b.getXBogus(query)[0]
        url = url + x_params

        res = await self.request.app.ctx.curl_client.http_get(url, headers=headers, proxy=proxy,
                                                              requests_client="httpx")
        self.request.app.ctx.tiktok_search_item_ms_token = f"{res.cookies.get('msToken')}"
        return json_success_response(res.json())
