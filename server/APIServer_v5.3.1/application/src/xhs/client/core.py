#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：core.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 10:43 
'''
import time, urllib.parse

from loguru import logger

from application.src.xhs.client import xhs_request, BASE_HEADERS
from application.src.xhs.client.parameter import MOBILE_HEADERS, get_random_pc_ua, get_random_mobile_ua, FeedType
from application.src.xhs.client.utils import parse_note_detail, parse_note_detail_v3, get_search_id, parse_user_detail
from core import CustomException


async def handle_base(http_client, method, uri, data=None, params=None, domain=None, cookie="", proxy=None):
    try:
        if params:
            uri = f"{uri}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
        result = await xhs_request(http_client, method, uri, data, domain=domain, cookie=cookie, proxy=proxy)
        headers = dict(result.headers)
        try:
            result_body = result.json()
            result_headers = headers
        except Exception as e:
            logger.warning(f"响应解析JSON失败: {str(e)}")
            result_body = None
            result_headers = headers

        # 构建返回数据
        response_data = {
            "response_status": result.status_code,
            "response_body": result_body,
            "response_headers": result_headers,
        }
        return response_data
    except Exception as e:
        logger.error(f"请求处理失败: {str(e)}")
        raise e


async def get_note_detail(http_client, note_id, xsec_token=None, cookie="", proxy=None):
    url = "/api/sns/web/v1/feed"
    data = {
        "source_note_id": note_id,
        "image_formats": ["jpg", "webp", "avif"],
        "extra": {"need_body_topic": 1},
        "xsec_source": "pc_feed",
        "xsec_token": xsec_token,
    }

    return await handle_base(http_client, "post", url, data, cookie=cookie, proxy=proxy)


async def get_user_by_id(http_client, user_id, xsec_token="", cookie="", proxy=None):
    params = {"target_user_id": user_id, "xsec_token": xsec_token}
    return await handle_base(
        http_client,
        "get",
        "/api/sns/web/v1/user/otherinfo",
        params=params,
        cookie=cookie,
        proxy=proxy
    )


async def get_user_detail_v2(http_client, user_id, xsec_token="", cookie="", proxy=None):
    url = f"https://www.xiaohongshu.com/user/profile/{user_id}?xsec_token={xsec_token}&xsec_source=pc_feed"
    headers = BASE_HEADERS.copy()
    headers.update({
        "cookie": cookie,
        "User-Agent": get_random_pc_ua()
    })
    response = await http_client.http_get(url=url, headers=headers, proxy=proxy)
    if response.status_code != 200:
        logger.warning(f"获取用户v2页面响应状态码异常: {response.status_code}")
        raise CustomException(f"获取用户v2页面响应状态码异常: {response.status_code}")

    user_data = await parse_user_detail(response.text)
    if not user_data:
        raise CustomException(message="解析用户详情失败")
    return user_data


async def get_any_account(http_client, cookie="", proxy=None):
    data = {}
    return await handle_base(
        http_client,
        "post",
        "/api/sns/web/v1/login/activate",
        data=data,
        cookie=cookie,
        proxy=proxy
    )


async def get_user_notes(http_client, user_id, xsec_token, cursor="", cookie="", proxy=None):
    params = {
        "num": 30,
        "cursor": cursor,
        "user_id": user_id,
        "image_formats": "jpg,webp,avif",
        "xsec_token": xsec_token,
        "xsec_source": "pc_feed"
    }
    return await handle_base(
        http_client,
        "get",
        "/api/sns/web/v1/user_posted",
        params=params,
        cookie=cookie,
        proxy=proxy
    )


async def get_note_detail_v2(http_client, note_id, xsec_token=None, cookie="", proxy=None):
    url = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed"
    headers = BASE_HEADERS.copy()
    headers.update({
        "cookie": cookie,
        "User-Agent": get_random_pc_ua()
    })
    response = await http_client.http_get(url=url, headers=headers, proxy=proxy)

    if response.status_code != 200:
        logger.warning(f"获取笔记v2页面响应状态码异常: {response.status_code}")
        raise CustomException(f"获取笔记v2页面响应状态码异常: {response.status_code}")

    note_data = await parse_note_detail(response.text)
    if not note_data:
        raise CustomException(message="解析笔记详情失败")

    return note_data


async def get_note_detail_v3(http_client, url, proxy=None):
    headers = MOBILE_HEADERS.copy()
    headers["User-Agent"] = get_random_mobile_ua()

    response = await http_client.http_get(
        url=url,
        headers=headers,
        proxy=proxy,
        allow_redirects=True
    )

    if response.status_code != 200:
        logger.warning(f"获取笔记v3页面响应状态码异常: {response.status_code}")
        raise CustomException(message=f"获取笔记v3页面响应状态码异常: {response.status_code}")
    note_data = await parse_note_detail_v3(response.text)
    if not note_data:
        raise CustomException(message="解析笔记详情v3失败")

    return note_data


async def get_search_note(http_client, keyword, page, page_size, sort, note_type, note_time, note_range, cookie, proxy):
    data = {
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
        "search_id": get_search_id(),
        "sort": "general",
        "note_type": "0",
        "ext_flags": [],
        "filters": [
            {"tags": [sort.value], "type": "sort_type"},
            {"tags": [note_type.value], "type": "filter_note_type"},
            {"tags": [note_time.value], "type": "filter_note_time"},
            {"tags": [note_range.value], "type": "filter_note_range"},
            {"tags": ["不限"], "type": "filter_pos_distance"}
        ],
        "geo": "",
        "image_formats": ["jpg", "webp", "avif"]
    }
    return await handle_base(http_client, "post", "/api/sns/web/v1/search/notes", data=data, cookie=cookie, proxy=proxy)


async def get_search_user(http_client, keyword, page=1, page_size=15, cookie="", proxy=None):
    data = {
        "search_user_request": {
            "keyword": keyword,
            "search_id": get_search_id(),
            "page": page,
            "page_size": page_size,
            "biz_type": "web_search_user",
            "request_id": f"{int(round(time.time()))}-{int(round(time.time() * 1000))}",
        }
    }
    return await handle_base(http_client, "post", "/api/sns/web/v1/search/usersearch", data=data, cookie=cookie,
                             proxy=proxy)


async def get_search_one_box(http_client, keyword, cookie="", proxy=None):
    data = {
        "keyword": keyword,
        "search_id": get_search_id(),
        "biz_type": "web_search_user",
        "request_id": f"{int(round(time.time()))}-{int(round(time.time() * 1000))}",
    }
    return await handle_base(http_client, "post", "/api/sns/web/v1/search/onebox", data=data, cookie=cookie,
                             proxy=proxy)


async def get_suggest_topic(http_client, keyword, page=1, cookie="", proxy=None):
    data = {
        "keyword": keyword,
        "suggest_topic_request": {"title": "", "desc": f"#{keyword}"},
        "page": {"page_size": 20, "page": page},
    }
    return await handle_base(http_client, "post", "/web_api/sns/v1/search/topic", data=data, cookie=cookie, proxy=proxy)


async def get_note_root_comment(http_client, note_id, cursor="", xsec_token=None, cookie="", proxy=None):
    params = {"note_id": note_id, "cursor": cursor, "image_formats": "jpg,webp,avif"}
    if xsec_token:
        params["xsec_token"] = xsec_token
    return await handle_base(http_client, "get", "/api/sns/web/v2/comment/page", params=params, cookie=cookie,
                             proxy=proxy)


async def get_note_sub_comments(http_client, note_id, root_comment_id, num=30, cursor="", xsec_token=None, cookie="",
                                proxy=None):
    params = {
        "note_id": note_id,
        "root_comment_id": root_comment_id,
        "num": num,
        "cursor": cursor,
        "image_formats": "jpg,webp,avif"
    }
    if xsec_token:
        params["xsec_token"] = xsec_token
    return await handle_base(http_client, "get", "/api/sns/web/v2/comment/sub/page", params=params, cookie=cookie,
                             proxy=proxy)


async def get_home_feed(http_client, feed_type=FeedType.RECOMMEND, cursor_score="", note_index=0, cookie="",
                        proxy=None):
    data = {
        "cursor_score": cursor_score,
        "num": 40,
        "refresh_type": 1,
        "note_index": note_index,
        "unread_begin_note_id": "",
        "unread_end_note_id": "",
        "unread_note_count": 0,
        "category": feed_type.value,
        "search_key": "",
        "need_num": 40,
        "image_scenes": ["jpg", "webp", "avif"]
    }
    return await handle_base(http_client, "post", "/api/sns/web/v1/homefeed", data=data, cookie=cookie, proxy=proxy)


async def get_search_suggest(http_client, keyword, cookie, proxy=None):
    params = {"keyword": urllib.parse.quote(keyword), "count": "15"}
    return await handle_base(http_client, "get", "/api/sns/web/v1/search/recommend", params=params, cookie=cookie,
                             proxy=proxy)


async def get_qrcode(http_client, cookie="", proxy=None):
    data = {}
    return await handle_base(http_client, "post", "/api/sns/web/v1/login/qrcode/create", data=data, cookie=cookie,
                             proxy=proxy)


async def check_qrcode(http_client, qr_id, code, cookie="", proxy=None):
    params = {"qr_id": qr_id, "code": code}
    return await handle_base(http_client, "get", "/api/sns/web/v1/login/qrcode/status", params=params, cookie=cookie,
                             proxy=proxy)


async def qrcode_captcha_init(http_client, verify_biz, verify_type, verify_uuid, sourceSite="", cookie="", proxy=None):
    data = {"verifyType": verify_type, "verifyUuid": verify_uuid, "verifyBiz": int(verify_biz),
            "sourceSite": sourceSite}

    return await handle_base(http_client, "post", "/api/redcaptcha/v2/qr/init", data=data, cookie=cookie,
                             proxy=proxy)


async def query_qrcode_captcha(http_client, rid, verify_biz, verify_type, verify_uuid, sourceSite="", cookie="",
                               proxy=None):
    data = {"verifyType": verify_type, "verifyUuid": verify_uuid, "verifyBiz": int(verify_biz),
            "sourceSite": sourceSite, "rid": rid}

    return await handle_base(http_client, "post", "/api/redcaptcha/v2/qr/status/query", data=data, cookie=cookie,
                             proxy=proxy)


async def login_send_code(http_client, mobile, cookie="", proxy=None):
    params = {"phone": mobile, "zone": "86", "type": "login"}
    return await handle_base(http_client, "get", "/api/sns/web/v2/login/send_code", params=params, cookie=cookie,
                             proxy=proxy)


async def login_check_code(http_client, mobile, code, cookie="", proxy=None):
    params = {"phone": mobile, "zone": "86", "code": code}
    return await handle_base(http_client, "get", "/api/sns/web/v1/login/check_code", params=params, cookie=cookie,
                             proxy=proxy)


async def login_check_status(http_client, mobile, mobile_token, cookie="", proxy=None):
    data = {"mobile_token": mobile_token, "zone": "86", "phone": mobile}
    return await handle_base(http_client, "post", "/api/sns/web/v2/login/code", data=data, cookie=cookie, proxy=proxy)


async def get_mobile_login_qr_code(http_client, verifyUuid, cookie="", proxy=None):
    data = {
        "verifyType": "209",
        "verifyUuid": verifyUuid,
        "verifyBiz": "471",
        "biz": "sns_web",
        "sourceSite": "https://www.xiaohongshu.com/explore/"}
    return await handle_base(http_client, "post", "/api/redcaptcha/v2/qr/init", data=data, cookie=cookie, proxy=proxy)


async def login_mobile_verify_qr_query(http_client, verifyUuid, rid, cookie, proxy=None):
    data = {
        "verifyType": "209",
        "verifyUuid": verifyUuid,
        "verifyBiz": "471", "biz": "sns_web",
        "sourceSite": "https://www.xiaohongshu.com/explore/",
        "rid": rid}
    return await handle_base(http_client, "post", "/api/redcaptcha/v2/qr/status/query", data=data, cookie=cookie,
                             proxy=proxy)


async def me_info(http_client, cookie="", proxy=None):
    return await handle_base(http_client, "get", "/api/sns/web/v1/user/selfinfo", cookie=cookie, proxy=proxy)


async def me_info_v2(http_client, cookie="", proxy=None):
    return await handle_base(http_client, "get", "/api/sns/web/v2/user/me", cookie=cookie, proxy=proxy)


async def get_mentions(http_client, num='20', cursor='', cookie="", proxy=None):
    params = {"num": num, "cursor": cursor}
    return await handle_base(http_client, "get", "/api/sns/web/v1/you/mentions", params=params, cookie=cookie,
                             proxy=proxy)


async def get_likes(http_client, num='20', cursor='', cookie="", proxy=None):
    params = {"num": num, "cursor": cursor}
    return await handle_base(http_client, "get", "/api/sns/web/v1/you/likes", params=params, cookie=cookie, proxy=proxy)


async def get_connections(http_client, num='20', cursor='', cookie="", proxy=None):
    params = {"num": num, "cursor": cursor}
    return await handle_base(http_client, "get", "/api/sns/web/v1/you/connections", params=params, cookie=cookie,
                             proxy=proxy)


async def get_share_code(http_client, note_id: str, cookie="", proxy=None):
    data = {"share_code": {"id": note_id}}
    return await handle_base(http_client, "post", "/api/sns/web/share/code", data=data, cookie=cookie, proxy=proxy)


async def get_note_short_link(http_client, note_id: str, cookie="", proxy=None):
    data = {"original_url": f"https://www.xiaohongshu.com/discovery/item/{note_id}"}
    return await handle_base(http_client, "post", "/api/sns/web/short_url", data=data, cookie=cookie, proxy=proxy)


async def get_view_note(http_client, note_id: str, note_type: int = 1, cookie="", proxy=None):
    data = {
        "note_id": note_id,
        "note_type": note_type,
        "report_type": 3,
        "stress_test": False,
        "trace": {
            "request_id": ""
        },
        "viewer": {},
        "author": {},
        "interaction": {
            "like": 0,
            "collect": 0,
            "comment": 0,
            "comment_read": 0
        },
        "note": {
            "stay_seconds": 0
        },
        "other": {
            "platform": "web"
        }
    }
    return await handle_base(http_client, "post", "/api/sns/web/v1/note/metrics_report", data=data, cookie=cookie,
                             proxy=proxy)


async def creator_cookie(http_client, cookie="", proxy=None):
    data = {
        "service": "https://creator.xiaohongshu.com",
        "source": "official",
        "type": "tgt"
    }
    return await handle_base(http_client, "post", domain="https://customer.xiaohongshu.com",
                             uri="/api/cas/customer/web/service-ticket", data=data, cookie=cookie,
                             proxy=proxy)
