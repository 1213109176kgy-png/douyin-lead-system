#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 9:30 
'''
import time

from bilibili_api import request_settings, Credential, user, search, comment, opus, rank
from bilibili_api.comment import OrderType
from bilibili_api.rank import RankType
from bilibili_api.user import VideoOrder
from sanic import Request, HTTPResponse
from typing import Optional, Dict, Any

from application.src.bilibili.client.base import BaseView
from application.src.bilibili.client.parameter import BASE_MOBILE_HEADERS
from core import CustomException, json_success_response
from libs import get_request_proxy


class AwemeDetailView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (bvid := data.get("bvid")):
            raise CustomException()

        base_url = f"https://www.bilibili.com/video/{bvid}/"
        headers = await self._headers(request)
        response = await self.fetch_data(request, base_url, headers)

        if not (result := await self.parse_script(
                response,
                r"<script>window.__INITIAL_STATE__=(.*?);\(function\(\)"
        )):
            raise CustomException(message="获取内容失败")

        return json_success_response(result)


class AwemeDetailV2View(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (bvid := data.get("bvid")):
            raise CustomException()

        base_url = f"https://api.bilibili.com/x/web-interface/wbi/view/detail"
        params = {
            "platform": "web",
            "bvid": bvid,
            "aid": "",
            "need_operation_card": "1",
            "web_rm_repeat": "1",
            "need_elec": "1",
            "page_no": "1",
            "p": "1",
            "web_location": "1446382",
            "gaia_source": "main_web",
            "from_spmid": "333.1387.upload.video_card.click",
            "spmid": "333.788.0.0",
            "from_trackid": "",
            "wts": f"{int(time.time())}"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "origin": "https://www.bilibili.com",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.bilibili.com/",
            "accept-language": "zh-CN,zh;q=0.9",
            "priority": "u=1, i",
        }
        proxy = await get_request_proxy(request)
        cookie = await self.get_buvid3(request, proxy=proxy)
        headers['cookie'] = cookie
        response = await self.fetch_data(request, url=base_url, headers=headers, params=params)

        result = response.json()

        return json_success_response(result)


class AwemeCardDetailView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not all((aid := data.get("aid"), bvid := data.get("bvid"), cid := data.get("cid"))):
            raise CustomException()

        base_url = (
            f"https://api.bilibili.com/x/player/wbi/playurl?"
            f"avid={aid}&bvid={bvid}&cid={cid}&qn=80&fnver=0&fnval=4048&fourk=1&"
            f"gaia_source=&from_client=BROWSER&is_main_page=true&"
            f"need_fragment=false&isGaiaAvoided=false&voice_balance=1"
        )

        headers = await self._headers(request)
        headers.update({
            "Host": "api.bilibili.com",
            "Referer": f"https://www.bilibili.com/video/{bvid}"
        })

        response = await self.fetch_data(request, url=base_url, headers=headers)
        return json_success_response(response.json())


class AwemeDownloadView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not all((avid := data.get("avid"), bvid := data.get("bvid"), cid := data.get("cid"))):
            raise CustomException()

        base_url = (
            f"https://api.bilibili.com/x/player/wbi/playurl?"
            f"avid={avid}&bvid={bvid}&cid={cid}&qn=80&fnver=0&fnval=4048&fourk=1&"
            f"gaia_source=&from_client=BROWSER&is_main_page=true&"
            f"need_fragment=false&isGaiaAvoided=false&voice_balance=1&dm_img_list="
        )

        headers = BASE_MOBILE_HEADERS.copy()
        if cookie := data.get("cookie"):
            headers["cookie"] = cookie

        response = await self.fetch_data(request, url=base_url, headers=headers)
        return json_success_response(response.json())


class UserALLPostView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (cookie := data.get("cookie")):
            raise CustomException()

        if not (user_id := data.get("user_id")):
            raise CustomException()

        offset = data.get("offset", "")

        headers = BASE_MOBILE_HEADERS.copy()
        headers["cookie"] = cookie

        base_url = (
            f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?"
            f"offset={offset}&host_mid={user_id}&timezone_offset=-480&platform=web&"
            f"features=itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,"
            f"forwardListHidden,decorationCard,commentsNewVersion,onlyfansAssetsV2,"
            f"ugcDelete,onlyfansQaCard&web_location=333.1387"
        )

        response = await self.fetch_data(request, base_url, headers=headers)
        return json_success_response(response.json())


class UserALLPostV2View(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (uid := data.get("uid")):
            raise CustomException()

        offset = data.get("offset")
        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)

        u = user.User(uid, credential=Credential())
        try:
            result = await u.get_dynamics_new(offset=offset)
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)


class GetOpusDetailView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (opus_id := data.get("opus_id")):
            raise CustomException()

        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)

        op = opus.Opus(opus_id=opus_id)
        try:
            result = await op.get_info()
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)


class SearchView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (keyword := data.get("keyword")):
            raise CustomException()

        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)

        search_type, order_type = self.get_search_type_and_order(
            data.get("search_type"),
            data.get("order_type")
        )
        time_range = data.get("time_range", -1)
        time_start = data.get("time_start", None)
        time_end = data.get("time_end", None)
        try:
            result = await search.search_by_type(
                keyword,
                search_type=search_type,
                order_type=order_type,
                time_range=time_range,
                time_start=time_start,
                time_end=time_end,
                order_sort=data.get("order_sort"),
                page=data.get("page")
            )
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)


class CommentsDataView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (aid := data.get("aid")):
            raise CustomException()

        order = OrderType.LIKE if data.get("order") == 'like' else OrderType.TIME
        page = data.get("page") or "1"

        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)

        credential = None
        if cookie := data.get("cookie"):
            cookie_dict = self.parse_cookie(cookie)
            if not self.check_cookie(cookie_dict):
                raise CustomException(message="请检查cookie的完整性，至少包含buvid3、SESSDATA、bili_jct")
            credential = Credential(
                sessdata=cookie_dict['SESSDATA'],
                bili_jct=cookie_dict['bili_jct'],
                buvid3=cookie_dict['buvid3']
            )

        try:
            result = await comment.get_comments_lazy(
                int(aid),
                comment.CommentResourceType.VIDEO,
                offset=page,
                credential=credential,
                order=order
            )
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)


class UserInfoView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (uid := data.get("uid")):
            raise CustomException()

        base_url = f"https://m.bilibili.com/space/{uid}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "referer": "https://m.bilibili.com/"
        }

        if cookie := data.get("cookie"):
            headers["Cookie"] = cookie

        response = await self.fetch_data(request, url=base_url, headers=headers)

        if not (result := await self.parse_script(
                response,
                r"<script>window.__INITIAL_STATE__=(.*?);\(function\(\)"
        )):
            raise CustomException(message="获取信息失败")

        try:
            user_stat = await self.fetch_data(
                request,
                f"https://api.bilibili.com/x/relation/stat?vmid={uid}&web_location=333.2",
                headers=headers
            )
            up_stat = await self.fetch_data(
                request,
                f"https://api.bilibili.com/x/space/upstat?mid={uid}&web_location=333.999",
                headers=headers
            )
            result['stat'] = user_stat.json()['data']
            result['up_stat'] = up_stat.json()['data']
        except (KeyError, Exception):
            pass

        return json_success_response(result)


class UserVideoListView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not (uid := data.get("uid")):
            raise CustomException()

        order_mapping = {
            'pubdate': VideoOrder.PUBDATE,
            'stow': VideoOrder.FAVORITE,
            None: VideoOrder.VIEW
        }
        order = order_mapping.get(data.get("order"))

        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)

        u = user.User(uid, credential=Credential())
        try:
            result = await u.get_videos(
                tid=data.get("tid"),
                pn=int(data.get("page", 1)),
                order=order,
                keyword=data.get("keyword")
            )
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)


class DownloadViewV2View(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        if not all((avid := data.get("avid"), bvid := data.get("bvid"), cid := data.get("cid"))):
            raise CustomException()

        base_url = (
            f"https://api.bilibili.com/x/player/playurl?"
            f"qn=120&gaia_source=app&isGaiaAvoided=true&"
            f"avid={avid}&bvid={bvid}&cid={cid}"
        )

        headers = {
            "referer": "https://api.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
        }

        response = await self.fetch_data(request, url=base_url, headers=headers)
        return json_success_response(response.json())


class PopularView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:
        base_url = f"https://api.bilibili.com/x/web-interface/popular?ps=20&pn={data.get('pn') or '1'}&web_location=333.934"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://www.bilibili.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bilibili.com/v/popular/all",
            "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

        response = await self.fetch_data(request, url=base_url, headers=headers)
        return json_success_response(response.json())


class RankView(BaseView):
    async def process_request(self, request: Request, data: Dict[str, Any]) -> HTTPResponse:

        proxy = await get_request_proxy(request)
        request.ctx.request_proxy = proxy
        request_settings.set_proxy(proxy)
        type_value = data.get("type") or None
        if type_value is None:
            rank_type = RankType.All
        else:
            rank_type = getattr(RankType, type_value, RankType.All)
        try:
            result = await rank.get_rank(type_=rank_type)
        except Exception as e:
            raise CustomException(message=str(e))

        return json_success_response(result)
