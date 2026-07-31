#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：__init__.py.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 9:57 
'''
import json
import re
import time
import traceback
import urllib.parse

from loguru import logger

import application.config

from application.src.xhs.args.client import Xhshow
from application.src.xhs.client.parameter import BASE_HEADERS, get_random_pc_ua
from core import CustomException


async def sign(http_client, url, data, cookie, retry=2):
    # 获取签名 自行搭建签名服务  根据args里的签名源码配置接收参数
    sig_req_data = {
        "path": url,
        "data": json.dumps(data),
        "cookie": cookie
    }
    xs_origin = application.config.BaseConfig.XHS_X_S_ORIGIN

    for attempt in range(retry + 1):
        try:
            sig_data = await http_client.http_post(url=xs_origin, data=sig_req_data, proxy=None)
            data = sig_data.json()
            if not data or 'data' not in data:
                logger.error(f"小红书签名返回数据格式错误: {data}")
                if attempt < retry:
                    logger.info(f"尝试重新获取签名, 重试 {attempt + 1}/{retry}")
                    time.sleep(1)
                    continue
                raise CustomException(message="小红书签名服务返回数据格式错误")
            return data['data']
        except Exception as e:
            logger.error(f"小红书签名请求失败: {str(e)}")
            if attempt < retry:
                logger.info(f"尝试重新获取签名, 重试 {attempt + 1}/{retry}")
                time.sleep(1)
                continue
            logger.error(f"签名失败详细信息: {traceback.format_exc()}")
            raise CustomException(message=f"小红书签名失败: {str(e)}, 请检查node环境和签名服务！")

def extract_a1_cookie_regex(cookie_str):
    pattern = r'a1=([^;]+)'
    match = re.search(pattern, cookie_str)
    if match:
        return match.group(1)
    return None



sign_client = Xhshow()


def sign_xs(uri, a1_value, payload):
    signature = sign_client.sign_xs(uri, a1_value, payload, method="GET")
    return signature


def post_xs(api, cookie, data):
    signature = sign_client.sign_headers_post(
        uri=api,
        cookies=cookie,
        payload=data
    )
    return signature


def get_xs(api, cookie, data):
    signature = sign_client.sign_headers_get(
        uri=api,
        cookies=cookie,
        params=data
    )
    return signature


def generate_xs_xs_common(api, cookie, data, method):
    if method == "GET":
        return get_xs(api, cookie, data)
    elif method == "POST":
        return post_xs(api, cookie, data)
    return None




async def xhs_request(http_client, method, url, data="", domain=None, cookie='', proxy=None, retry=2):
    if not cookie:
        raise CustomException(message="请求需要cookie参数")
    a1 = extract_a1_cookie_regex(cookie)
    # print(data)
    if data:
        data = data
    else:
        parsed_url = urllib.parse.urlparse(url)
        data = dict(urllib.parse.parse_qsl(parsed_url.query, keep_blank_values=True))
    try:
        client = generate_xs_xs_common(url, data=data, cookie=cookie, method=method.upper())
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(f"小红书签名失败: {str(e)}")
        logger.error(f"签名失败详细信息: {traceback.format_exc()}")
        raise CustomException(message=f"小红书签名失败: {str(e)}, 请检查node环境是否正常")

    headers = BASE_HEADERS.copy()
    headers["User-Agent"] = get_random_pc_ua()
    headers.update({
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'Host': 'edith.xiaohongshu.com',
        'Sec-Ch-Ua': '"Chromium";v="120", "Not(A:Brand";v="24", "Microsoft Edge";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        "Cookie": cookie,
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive'
    })
    headers.update(client)

    for attempt in range(retry + 1):
        try:
            if method.lower() == "post":
                data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
                data_str = data_str.strip('"').replace("\\", "")
                url_domain = domain if domain else "https://edith.xiaohongshu.com"
                req = await http_client.http_post(
                    url=url_domain + url,
                    data=data_str.encode("utf-8"),
                    headers=headers,
                    proxy=proxy
                )
            else:
                req = await http_client.http_get(
                    url="https://edith.xiaohongshu.com" + url,
                    headers=headers,
                    proxy=proxy
                )

            if req.status_code in [429, 403, 503]:
                logger.warning(f"遇到请求限制 状态码:{req.status_code}, 重试 {attempt + 1}/{retry}")
                if attempt < retry:
                    wait_time = 1 * (2 ** attempt)
                    time.sleep(wait_time)
                    headers["User-Agent"] = get_random_pc_ua()
                    continue

            return req

        except Exception as e:
            logger.error(f"请求失败: {str(e)}")
            if attempt < retry:
                logger.info(f"重试请求, 第 {attempt + 1}/{retry} 次")
                time.sleep(1)
                continue
            raise e
