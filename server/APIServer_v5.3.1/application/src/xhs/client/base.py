#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：client.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 10:00 
'''
import re
from urllib.parse import parse_qs

from loguru import logger

from application.config import BaseConfig
from application.src.xhs.client.core import get_user_by_id, get_any_account, get_user_notes, \
    get_note_detail_v2, get_note_detail, get_note_detail_v3, get_search_note, get_search_user, get_note_root_comment, \
    get_note_sub_comments, get_home_feed, get_search_suggest, get_suggest_topic, get_qrcode, check_qrcode, \
    login_send_code, login_check_code, login_check_status, get_mobile_login_qr_code, login_mobile_verify_qr_query, \
    get_user_detail_v2, me_info, me_info_v2, get_mentions, get_likes, get_connections, get_share_code, \
    get_note_short_link, get_search_one_box, get_view_note, qrcode_captcha_init, query_qrcode_captcha, creator_cookie
from application.src.xhs.client.parameter import BASE_HEADERS, SearchSortType, SearchNoteType, FeedType, SearchNoteTime, \
    SearchNoteRange
from application.src.xhs.client.utils import extract_id, get_a1_and_web_id, get_secpoisonid, qr_to_base64, \
    remove_web_session, extract_cookies
from core import CustomException
from libs import get_request_proxy


class BaseClient:

    def __init__(self, request):
        self.request = request
        self.request_data = self.request.ctx.request_data
        self.http_client = self.request.app.ctx.curl_client
        self.item_pattern = r'/(explore|item)/([a-zA-Z0-9]+)(?:.*xsec_token=([\w=-]+))?'
        self.need_ck_message = "请携带cookie进行请求"

    async def _fetch_url(self, url: str, headers: dict):
        try:
            response = await self.http_client.http_get(url, headers=headers, allow_redirects=False)
            location = response.headers.get('location')
            if not location:
                raise CustomException(message="获取url失败, 请检查分享链接是否可用")
            return str(location)
        except Exception as e:
            logger.error(f"获取跳转链接失败: {str(e)}")
            raise CustomException(message=f"获取url失败: {str(e)}")

    @staticmethod
    async def extract_url(url_text: str):
        try:
            urls = re.findall('http[s]?://[^ ]+', url_text)
            if not urls:
                raise CustomException(message="未找到有效的url链接")
            return urls
        except Exception as e:
            logger.error(f"提取URL失败: {str(e)}")
            raise CustomException(message="未找到有效的url链接")

    async def get_note_id(self, share_text: str):
        try:
            url = await self.extract_url(share_text)
            if not url:
                return None
            url = url[0]
            if "/explore/" in url or "/discovery/item/" in url:
                return await extract_id(url, self.item_pattern)
            headers = BASE_HEADERS.copy()
            url = await self._fetch_url(url, headers)
            return await extract_id(url, self.item_pattern)
        except Exception as e:
            logger.error(f"获取笔记ID失败: {str(e)}")
            raise e

    async def get_ab_request_id_and_acw_tc(self, proxy):
        headers = BASE_HEADERS.copy()
        response = await self.http_client.http_get("https://www.xiaohongshu.com/explore", headers=headers, proxy=proxy)
        ab_request_id = response.cookies.get('abRequestId', "")
        acw_tc = response.cookies.get('acw_tc', "")
        return ab_request_id, acw_tc

    @staticmethod
    async def get_user_id(share_text: str):
        try:
            url = re.findall('http[s]?://[^ ]+', share_text)
            if not url:
                return None
            url = url[0]
            return await extract_id(url, r'/profile/([a-zA-Z0-9]+)(?:.*xsec_token=([\w=-]+))?')
        except Exception as e:
            logger.error(f"获取用户ID失败: {str(e)}")
            raise CustomException(message=f"获取用户ID失败: {str(e)}")

    async def use_any_account(self, cookie):
        if cookie:
            return cookie
        if BaseConfig.XHS_NOTE_DETAIL_USE_ANYACCOUNT:
            try:
                cookie_data = await self.any_account()
                return cookie_data['response_body']['data']['cookie']
            except Exception as e:
                logger.error(f"获取匿名cookie失败: {str(e)}")
                raise e
        else:
            raise CustomException(message=self.need_ck_message)

    async def note_detail(self):
        note_id = self.request_data.get("note_id", None)
        share_text = self.request_data.get("share_text", None)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        proxy = await get_request_proxy(self.request)

        if not cookie:
            raise CustomException(message=self.need_ck_message)
        if not note_id:
            if not share_text:
                raise CustomException(message="缺少note_id或share_text参数")
            try:
                id_group = await self.get_note_id(share_text=share_text)
                if not id_group:
                    raise CustomException(message="分享链接错误")
                note_id = id_group[0]
                xsec_token = id_group[1]
            except Exception as e:
                raise CustomException(message=f"从分享链接解析ID失败: {str(e)}")

            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")
        else:
            xsec_token = self.request_data.get("xsec_token", None)
            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")

        try:
            response_data = await get_note_detail(
                http_client=self.http_client,
                note_id=note_id,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取笔记详情失败: {str(e)}")
            raise e

    async def note_detail_v2(self):
        note_id = self.request_data.get("note_id", None)
        share_text = self.request_data.get("share_text", None)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        proxy = await get_request_proxy(self.request)
        if not note_id:
            if not share_text:
                raise CustomException(message="缺少note_id或share_text参数")
            try:
                id_group = await self.get_note_id(share_text=share_text)
                if not id_group:
                    raise CustomException(message="分享链接错误")
                note_id = id_group[0]
                xsec_token = id_group[1]
            except Exception as e:
                raise CustomException(message=f"从分享链接解析ID失败: {str(e)}")

            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")
        else:
            xsec_token = self.request_data.get("xsec_token", None)
            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")

        try:
            response_data = await get_note_detail_v2(
                http_client=self.http_client,
                note_id=note_id,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取笔记详情v2失败: {str(e)}")
            raise e

    async def note_detail_v3(self):
        try:
            share_text = self.request_data.get("share_text", None)
            if not share_text:
                raise CustomException(message="缺少share_text参数")

            url = await self.extract_url(share_text)
            proxy = await get_request_proxy(self.request)

            response_data = await get_note_detail_v3(
                http_client=self.http_client,
                url=url[0],
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取笔记详情v3失败: {str(e)}")
            raise e

    async def user_detail(self):
        user_id = self.request_data.get("user_id", None)
        xsec_token = self.request_data.get("xsec_token", None)
        share_text = self.request_data.get("share_text", None)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        proxy = await get_request_proxy(self.request)
        if not cookie:
            raise CustomException(message=self.need_ck_message)
        if not user_id:
            if not share_text:
                raise CustomException(message="缺少user_id或share_text参数")
            try:
                user_id, xsec_token = await self.get_user_id(share_text=share_text)
                if not user_id:
                    raise CustomException(message="从分享链接解析用户ID失败")
            except Exception as e:
                raise CustomException(message=f"从分享链接解析用户ID失败: {str(e)}")

        try:
            xsec_token = xsec_token if xsec_token else ""
            response_data = await get_user_by_id(
                http_client=self.http_client,
                user_id=user_id,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取用户详情失败: {str(e)}")
            raise CustomException(message=f"获取用户详情失败: {str(e)}")

    async def user_detail_v2(self):
        user_id = self.request_data.get("user_id", None)
        xsec_token = self.request_data.get("xsec_token", None)
        share_text = self.request_data.get("share_text", None)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        proxy = await get_request_proxy(self.request)
        if not cookie:
            raise CustomException(message=self.need_ck_message)
        if not user_id:
            if not share_text:
                raise CustomException(message="缺少user_id或share_text参数")
            try:
                user_id, xsec_token = await self.get_user_id(share_text=share_text)
                if not user_id:
                    raise CustomException(message="从分享链接解析用户ID失败")
            except Exception as e:
                raise CustomException(message=f"从分享链接解析用户ID失败: {str(e)}")

        try:
            xsec_token = "" if not xsec_token else xsec_token
            response_data = await get_user_detail_v2(
                http_client=self.http_client,
                user_id=user_id,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取用户详情失败: {str(e)}")
            raise e

    async def any_account(self):
        retries = 0
        while retries <= 6:
            try:
                proxy = await get_request_proxy(self.request)
                a1, web_id = get_a1_and_web_id()
                secpoisonid = await get_secpoisonid()
                cookie = f"webBuild=4.62.3;xsecappid=xhs-pc-web;a1={a1};webId={web_id};sec_poison_id={secpoisonid}"
                response_data = await get_any_account(
                    http_client=self.http_client,
                    cookie=cookie,
                    proxy=proxy
                )
                response_body = response_data.get("response_body", None)
                if response_body.get("data") and response_body.get("code") == 0:
                    session_value = response_body["data"].get("session")
                    session = f"web_session={session_value};"

                    set_cookie = response_data['response_headers'].get('set-cookie', '')
                    acw_tc_match = re.search(r"acw_tc=([^;]+)", set_cookie)

                    if acw_tc_match:
                        acw_tc = acw_tc_match.group(1)
                        response_data['response_body']['data']['cookie'] = session + cookie + f";acw_tc={acw_tc}"
                    else:
                        response_data['response_body']['data']['cookie'] = session + cookie
                    return response_data
                else:
                    logger.error(f"获取匿名cookie响应异常: {response_body}")
                    retries += 1
                    continue
            except Exception as e:
                logger.error(e)
                raise e

        raise CustomException(message="获取匿名cookie失败，请稍后再试")

    async def user_post(self):
        user_id = self.request_data.get("user_id", None)
        cursor = self.request_data.get("cursor", "")
        share_text = self.request_data.get("share_text", None)
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        if not cookie:
            raise CustomException(message=self.need_ck_message)
        if not user_id:
            if not share_text:
                raise CustomException(message="缺少user_id或share_text参数")
            try:
                user_id = await self.get_user_id(share_text=share_text)
                if not user_id:
                    raise CustomException(message="从分享链接解析用户ID失败")
            except Exception as e:
                raise CustomException(message=f"从分享链接解析用户ID失败: {str(e)}")

        try:
            xsec_token = ""
            response_data = await get_user_notes(
                http_client=self.http_client,
                user_id=user_id,
                xsec_token=xsec_token,
                cursor=cursor,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取用户笔记失败: {str(e)}")
            raise e

    async def search_note(self):
        keyword = self.request_data.get("keyword", None)
        page = self.request_data.get("page", 1)
        page_size = self.request_data.get("page_size", 20)
        sort = self.request_data.get("sort", "general")
        note_type = self.request_data.get("note_type", "all")
        note_time = self.request_data.get("note_time", "不限")
        note_range = self.request_data.get("note_range", "不限")
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        if not keyword:
            raise CustomException(message="请传入搜索关键词")
        if not cookie:
            raise CustomException(message="请传入已登录的cookie")
        sort = {
            "hot": SearchSortType.MOST_POPULAR,
            "new": SearchSortType.LATEST,
            "comment": SearchSortType.COMMENT,
            "collect": SearchSortType.COLLECT,
        }.get(sort, SearchSortType.GENERAL)

        note_type = {
            "video": SearchNoteType.VIDEO,
            "image": SearchNoteType.IMAGE
        }.get(note_type, SearchNoteType.ALL)
        note_time = {
            "one_day": SearchNoteTime.ONE_DAY,
            "one_week": SearchNoteTime.ONE_WEEK,
            "half_year": SearchNoteTime.HALF_YEAR
        }.get(note_time, SearchNoteTime.NO_LIMIT)
        note_range = {
            "seen": SearchNoteRange.SEEN,
            "no_seen": SearchNoteRange.NO_SEEN,
            "followed": SearchNoteRange.FOLLOWED
        }.get(note_range, SearchNoteRange.NO_LIMIT)
        try:
            response_data = await get_search_note(
                http_client=self.http_client,
                keyword=keyword,
                page=page,
                page_size=page_size,
                sort=sort,
                note_type=note_type,
                note_time=note_time,
                note_range=note_range,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"搜索笔记失败: {str(e)}")
            raise e

    async def search_user(self):
        keyword = self.request_data.get("keyword", None)
        page = self.request_data.get("page", 1)
        page_size = self.request_data.get("page_size", 15)
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        if not keyword:
            raise CustomException(message="请传入搜索关键词")
        if not cookie:
            raise CustomException(message="请传入已登录的cookie")
        try:
            response_data = await get_search_user(
                http_client=self.http_client,
                keyword=keyword,
                page=page,
                page_size=page_size,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"搜索用户失败: {str(e)}")
            raise CustomException(message=f"搜索用户失败: {str(e)}")

    async def search_one_box(self):
        keyword = self.request_data.get("keyword", None)
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        if not keyword:
            raise CustomException(message="请传入搜索关键词")
        if not cookie:
            raise CustomException(message="请传入已登录的cookie")
        try:
            response_data = await get_search_one_box(
                http_client=self.http_client,
                keyword=keyword,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"搜索用户失败: {str(e)}")
            raise CustomException(message=f"搜索用户失败: {str(e)}")

    async def search_topic(self):
        keyword = self.request_data.get("keyword", None)
        page = self.request_data.get("page", 1)
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        if not keyword:
            raise CustomException(message="请传入搜索关键词")
        if not cookie:
            raise CustomException(message="请传入已登录的cookie")
        try:
            response_data = await get_suggest_topic(
                http_client=self.http_client,
                keyword=keyword,
                page=page,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"搜索话题失败: {str(e)}")
            raise CustomException(message=f"搜索话题失败: {str(e)}")

    async def note_root_comment(self):
        note_id = self.request_data.get("note_id", None)
        share_text = self.request_data.get("share_text", None)
        cursor = self.request_data.get("cursor", "")
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        # 检查cookie
        if not cookie:
            raise CustomException(message=self.need_ck_message)

        # 处理笔记ID和xsec_token
        if not note_id:
            if not share_text:
                raise CustomException(message="缺少note_id或share_text参数")
            try:
                id_group = await self.get_note_id(share_text=share_text)
                if not id_group:
                    raise CustomException(message="分享链接错误")
                note_id = id_group[0]
                xsec_token = id_group[1]
            except Exception as e:
                raise CustomException(message=f"从分享链接解析ID失败: {str(e)}")

            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")
        else:
            xsec_token = self.request_data.get("xsec_token", None)
            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")

        try:
            response_data = await get_note_root_comment(
                http_client=self.http_client,
                note_id=note_id,
                cursor=cursor,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取笔记父评论失败: {str(e)}")
            raise e

    async def note_sub_comment(self):
        note_id = self.request_data.get("note_id", None)
        share_text = self.request_data.get("share_text", None)
        root_comment_id = self.request_data.get("root_comment_id", None)
        cursor = self.request_data.get("cursor", "")
        cookie = self.request_data.get("cookie", None)
        proxy = await get_request_proxy(self.request)

        # 检查cookie
        if not cookie:
            raise CustomException(message=self.need_ck_message)
        if not root_comment_id:
            raise CustomException(message="缺少root_comment_id参数")
        # 处理笔记ID和xsec_token
        if not note_id:
            if not share_text:
                raise CustomException(message="缺少note_id或share_text参数")
            try:
                id_group = await self.get_note_id(share_text=share_text)
                if not id_group:
                    raise CustomException(message="分享链接错误")
                note_id = id_group[0]
                xsec_token = id_group[1]
            except Exception as e:
                raise CustomException(message=f"从分享链接解析ID失败: {str(e)}")

            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")
        else:
            xsec_token = self.request_data.get("xsec_token", None)
            if not xsec_token:
                raise CustomException(message="缺少xsec_token参数")

        try:
            response_data = await get_note_sub_comments(
                http_client=self.http_client,
                note_id=note_id,
                root_comment_id=root_comment_id,
                cursor=cursor,
                xsec_token=xsec_token,
                cookie=cookie,
                proxy=proxy
            )
            return response_data
        except Exception as e:
            logger.error(f"获取笔记子评论失败: {str(e)}")
            raise e

    async def home_feed(self):
        # 支持匿名cookie
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        proxy = await get_request_proxy(self.request)
        feed_type = self.request_data.get("feed_type", "0")
        cursor_score = self.request_data.get("cursor_score", "")
        feed_type = {
            "0": FeedType.RECOMMEND,
            "1": FeedType.FASION,
            "2": FeedType.FOOD,
            "3": FeedType.COSMETICS,
            "4": FeedType.MOVIE,
            "5": FeedType.CAREER,
            "6": FeedType.EMOTION,
            "7": FeedType.HOURSE,
            "8": FeedType.GAME,
            "9": FeedType.TRAVEL,
            "10": FeedType.FITNESS,
        }.get(feed_type, FeedType.RECOMMEND)
        try:
            response_data = await get_home_feed(http_client=self.http_client, feed_type=feed_type,
                                                cursor_score=cursor_score,
                                                cookie=cookie, proxy=proxy)
            return response_data

        except Exception as e:
            logger.error(f"获取首页推荐失败: {str(e)}")
            raise CustomException(message=f"获取首页推荐失败: {str(e)}")

    async def search_suggest(self):
        keyword = self.request_data.get("keyword", None)
        proxy = await get_request_proxy(self.request)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        if not keyword:
            raise CustomException(message="缺少keyword参数")
        try:
            response_data = await get_search_suggest(http_client=self.http_client, keyword=keyword, cookie=cookie,
                                                     proxy=proxy)
            return response_data

        except Exception as e:
            logger.error(f"获取联想关键词失败: {str(e)}")
            raise e

    async def qr_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        try:
            response_data = await get_qrcode(http_client=self.http_client, cookie=cookie, proxy=proxy)
            qr_url = response_data['response_body']['data']['url']
            response_data['response_body']['data']['base64_qr_code'] = await qr_to_base64(qr_url)
            cookie_str = "unread={%22ub%22:%2266e2f3690000000012011cb0%22%2C%22ue%22:%2266e823b9000000001e018443%22%2C%22uc%22:14};gid=yjJJWyiYfKMyyjJJWyiYYVIvqK2EfyMuuyMdE016fE2vSU286k88SE888yKJJq4800jJd8qq;"
            response_data['response_body']['data']['cookie'] = cookie_str + remove_web_session(cookie)
            return response_data

        except Exception as e:
            logger.error(f"获取登录二维码失败: {str(e)}")
            raise CustomException(message=f"获取登录二维码失败: {str(e)}")

    async def check_qr_code(self):
        proxy = await get_request_proxy(self.request)
        qr_id = self.request_data.get("qr_id", None)
        code = self.request_data.get("code", None)
        cookie = self.request_data.get("cookie", None)

        if not qr_id or not code or not cookie:
            raise CustomException(message="缺少qr_id、code或cookie参数")

        try:
            response_data = await check_qrcode(http_client=self.http_client, qr_id=qr_id, code=code, cookie=cookie,
                                               proxy=proxy)
            if "login_info" in response_data['response_body']['data']:
                if "session" in response_data['response_body']['data']['login_info']:
                    cookie_dict = {k: v[0] for k, v in parse_qs(cookie.replace('; ', '&')).items()}
                    cookie_dict['web_session'] = response_data['response_body']['data']['login_info']['session']
                    response_data['response_body']['cookie'] = "; ".join(
                        [f"{key}={value}" for key, value in cookie_dict.items()])
                    response_data['response_body']['cookie'].replace("web_session=;", "")
            return response_data

        except Exception as e:
            logger.error(f"获取登录二维码失败: {str(e)}")
            raise e

    async def qr_code_captcha_init(self):
        proxy = await get_request_proxy(self.request)
        sourceSite = self.request_data.get("sourceSite", "")
        verify_biz = self.request_data.get("verify_biz", None)
        verify_type = self.request_data.get("verify_type", None)
        verify_uuid = self.request_data.get("verify_uuid", None)
        cookie = self.request_data.get("cookie", None)
        if not verify_biz or not verify_type or not verify_uuid or not cookie:
            raise CustomException(message="参数缺失")

        response_data = await qrcode_captcha_init(http_client=self.http_client, sourceSite=sourceSite,
                                                  verify_biz=verify_biz, verify_type=verify_type,
                                                  verify_uuid=verify_uuid, cookie=cookie,
                                                  proxy=proxy)

        return response_data

    async def query_qr_code_captcha(self):
        proxy = await get_request_proxy(self.request)
        rid = self.request_data.get("rid", "")
        sourceSite = self.request_data.get("sourceSite", "")
        verify_biz = self.request_data.get("verify_biz", None)
        verify_type = self.request_data.get("verify_type", None)
        verify_uuid = self.request_data.get("verify_uuid", None)
        cookie = self.request_data.get("cookie", None)
        if not verify_biz or not verify_type or not verify_uuid or not cookie or not rid:
            raise CustomException(message="参数缺失")

        response_data = await query_qrcode_captcha(http_client=self.http_client, rid=rid, sourceSite=sourceSite,
                                                  verify_biz=verify_biz, verify_type=verify_type,
                                                  verify_uuid=verify_uuid, cookie=cookie,
                                                  proxy=proxy)

        return response_data

    async def mobile_login_send_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        mobile = self.request_data.get("mobile", None)
        if not mobile:
            raise CustomException(message="缺少mobile参数")

        try:
            response_data = await login_send_code(http_client=self.http_client, mobile=mobile, cookie=cookie,
                                                  proxy=proxy)
            response_data['cookie'] = remove_web_session(cookie, reserve_session=False)
            return response_data

        except Exception as e:
            logger.error(f"发送登录短信失败: {str(e)}")
            raise e

    async def mobile_login_check_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        mobile = self.request_data.get("mobile", None)
        code = self.request_data.get("code", None)

        if not cookie or not mobile or not code:
            raise CustomException(message="缺少mobile、code或cookie参数")

        try:
            response_data = await login_check_code(http_client=self.http_client, mobile=mobile, code=code,
                                                   cookie=cookie,
                                                   proxy=proxy)
            return response_data

        except Exception as e:
            logger.error(f"检查登录短信失败: {str(e)}")
            raise e

    async def mobile_login_check_status(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        mobile = self.request_data.get("mobile", None)
        mobile_token = self.request_data.get("mobile_token", None)

        if not cookie or not mobile or not mobile_token:
            raise CustomException(message="缺少mobile、mobile_token或cookie参数")

        try:
            response_data = await login_check_status(http_client=self.http_client, mobile=mobile,
                                                     mobile_token=mobile_token,
                                                     cookie=cookie, proxy=proxy)
            if response_data['response_status'] == 200 and response_data['response_body']['code'] == 0:
                cookie = f"web_session={response_data['response_body']['data']['session']};{cookie}".replace(
                    "web_session=;", "")
                response_data['cookie'] = cookie
            return response_data

        except Exception as e:
            logger.error(f"检查登录状态失败: {str(e)}")
            raise e

    async def mobile_login_qr_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        verifyUuid = self.request_data.get("verifyUuid", None)
        if not verifyUuid or not cookie:
            raise CustomException(message="缺少verifyUuid参数")
        try:
            response_data = await get_mobile_login_qr_code(http_client=self.http_client, verifyUuid=verifyUuid,
                                                           cookie=cookie,
                                                           proxy=proxy)
            rid = response_data['response_body']['data']['rid']
            response_data[
                'qr_code'] = f"xhsdiscover://rn/kuri/scan-confirm?rid={rid}&verifyUuid={verifyUuid}&verifyBiz=471&verifyType=209&webid="
            return response_data

        except Exception as e:
            logger.error(f"获取验证二维码失败: {str(e)}")
            raise e

    async def mobile_login_check_qr_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        verifyUuid = self.request_data.get("verifyUuid", None)
        rid = self.request_data.get("rid", None)
        if not verifyUuid or not rid or not cookie:
            raise CustomException(message="缺少verifyUuid, rid或cookie参数")
        try:
            response_data = await login_mobile_verify_qr_query(http_client=self.http_client, verifyUuid=verifyUuid,
                                                               rid=rid,
                                                               cookie=cookie,
                                                               proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"检查验证二维码失败: {str(e)}")
            raise e

    async def me_info(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await me_info(http_client=self.http_client, cookie=cookie, proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取个人信息失败: {str(e)}")
            raise e

    async def get_me_info_v2(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await me_info_v2(http_client=self.http_client, cookie=cookie, proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取个人信息_v2失败: {str(e)}")
            raise e

    async def ats_comment(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        num = self.request_data.get("num", "20")
        cursor = self.request_data.get("cursor", "")
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await get_mentions(http_client=self.http_client, num=num, cursor=cursor, cookie=cookie,
                                               proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取艾特和评论失败: {str(e)}")
            raise e

    async def likes(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        num = self.request_data.get("num", "20")
        cursor = self.request_data.get("cursor", "")
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await get_likes(http_client=self.http_client, num=num, cursor=cursor, cookie=cookie,
                                            proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取赞和收藏失败: {str(e)}")
            raise e

    async def connections(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        num = self.request_data.get("num", "20")
        cursor = self.request_data.get("cursor", "")
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await get_connections(http_client=self.http_client, num=num, cursor=cursor, cookie=cookie,
                                                  proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取新增关注失败: {str(e)}")
            raise e

    async def share_code(self):
        proxy = await get_request_proxy(self.request)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        note_id = self.request_data.get("note_id", "20")
        if not cookie or not note_id:
            raise CustomException(message="缺少cookie或note_id参数")
        try:
            response_data = await get_share_code(http_client=self.http_client, note_id=note_id, cookie=cookie,
                                                 proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取分享code失败: {str(e)}")
            raise e

    async def short_link(self):
        proxy = await get_request_proxy(self.request)
        cookie = await self.use_any_account(self.request_data.get("cookie", None))
        note_id = self.request_data.get("note_id", "20")
        if not cookie or not note_id:
            raise CustomException(message="缺少cookie或note_id参数")
        try:
            response_data = await get_note_short_link(http_client=self.http_client, note_id=note_id, cookie=cookie,
                                                      proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"获取短链失败: {str(e)}")
            raise e

    async def view_note(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        note_id = self.request_data.get("note_id", "20")
        if not cookie or not note_id:
            raise CustomException(message="缺少cookie或note_id参数")
        try:
            response_data = await get_view_note(http_client=self.http_client, note_id=note_id, cookie=cookie,
                                                proxy=proxy)

            return response_data

        except Exception as e:
            logger.error(f"增加播放失败: {str(e)}")
            raise e


    async def get_creator_cookie(self):
        proxy = await get_request_proxy(self.request)
        cookie = self.request_data.get("cookie", None)
        if not cookie:
            raise CustomException(message="缺少cookie参数")
        try:
            response_data = await creator_cookie(http_client=self.http_client, cookie=cookie, proxy=proxy)
            creator_cookie_str = response_data['response_headers']['set-cookie']
            cookie_str = extract_cookies(creator_cookie_str)
            response_data['cookie'] = cookie_str + cookie
            return response_data

        except Exception as e:
            logger.error(f"获取创作者cookie失败: {str(e)}")
            raise e