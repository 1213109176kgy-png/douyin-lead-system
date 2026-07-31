#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：common.py
@IDE     ：PyCharm 

@Date    ：2025/4/15 21:58 
'''
import asyncio
import json
import random
import re
from typing import Union, Dict, Any, List

import aiofiles
import execjs
import httpx
from loguru import logger

from libs import get_request_proxy


async def generate_ttwid(request) -> str:
    """
    生成请求必带的ttwid
    param :None
    return:ttwid
    """
    url = 'https://ttwid.bytedance.com/ttwid/union/register/'
    data = '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}'
    try:
        proxy = await get_request_proxy(request)
        response = await request.app.ctx.curl_client.http_post(url=url, data=data, proxy=proxy)
        for j, k in response.cookies.items():
            return k
    except Exception as e:
        raise e


async def generate_ttwid_so(request, keyword) -> str:
    url = 'https://so.douyin.com/s'
    params = {
        "search_entrance": "aweme",
        "keyword": keyword,
        "pd": "live",
        "innerWidth": "412",
        "innerHeight": "915",
        "is_no_width_reload": "0"
    }
    try:
        proxy = await get_request_proxy(request)
        response = await request.app.ctx.curl_client.http_get(url=url, params=params, proxy=proxy)
        for j, k in response.cookies.items():
            return k
    except Exception as e:
        raise e


def extract_json_from_string(
        text: str,
        merge_data: bool = True
) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
    json_data = _smart_extract_json_objects(text)

    # 如果不需要合并，直接返回JSON列表
    if not merge_data:
        return json_data

    # 合并JSON对象
    merged_dict = json_data[0].copy()

    # 确保data字段是列表
    if 'data' not in merged_dict:
        merged_dict['data'] = []
    elif not isinstance(merged_dict['data'], list):
        merged_dict['data'] = [merged_dict['data']]

    # 合并其余JSON对象
    for i in range(1, len(json_data)):
        json_obj = json_data[i]
        if 'data' in json_obj:
            if isinstance(json_obj['data'], list):
                merged_dict['data'].extend(json_obj['data'])
            else:
                merged_dict['data'].append(json_obj['data'])

        for key, value in json_obj.items():
            if key != 'data' and key not in merged_dict:
                merged_dict[key] = value

    return merged_dict


def _smart_extract_json_objects(text: str) -> List[Dict[str, Any]]:
    json_data = []

    braces_stack = []  # 用于跟踪大括号的栈
    potential_jsons = []  # 存储潜在的JSON对象
    start_positions = []

    for i, char in enumerate(text):
        if char == '{':
            if len(braces_stack) == 0:  # 新的顶层JSON对象开始
                start_positions.append(i)
            braces_stack.append(i)
        elif char == '}' and braces_stack:
            start = braces_stack.pop()
            if len(braces_stack) == 0:  # 顶层JSON对象结束
                potential_jsons.append(text[start:i + 1])

    for i, json_str in enumerate(potential_jsons):
        try:
            json_str = json_str.strip()
            if not json_str.startswith('{'):
                continue
            if not json_str.endswith('}'):
                continue

            try:
                json_obj = json.loads(json_str)
                json_data.append(json_obj)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON #{i + 1} 解析失败: {str(e)[:100]}...")
        except Exception as e:
            logger.warning(f"处理JSON字符串 #{i + 1} 时出错: {str(e)[:100]}...")

    if not json_data:

        lines = text.split('\n')
        is_json_line = False
        current_json = ""
        brace_count = 0

        for i, line in enumerate(lines):
            stripped_line = line.strip()

            if not stripped_line:
                continue

            if stripped_line.startswith('{') and not is_json_line:
                current_json = stripped_line
                is_json_line = True
                brace_count = stripped_line.count('{') - stripped_line.count('}')
            elif is_json_line:
                current_json += ' ' + stripped_line  # 添加空格，确保不破坏JSON结构
                brace_count += stripped_line.count('{') - stripped_line.count('}')

                if brace_count == 0:
                    try:
                        json_obj = json.loads(current_json)
                        json_data.append(json_obj)
                        current_json = ""
                        is_json_line = False
                    except json.JSONDecodeError:
                        if stripped_line.endswith('}'):
                            current_json = ""
                            is_json_line = False

    if not json_data:
        try:
            json_pattern = r'(\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
            matches = re.findall(json_pattern, text)

            for match in matches:
                try:
                    json_obj = json.loads(match)
                    json_data.append(json_obj)
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.warning(f"正则表达式提取失败: {str(e)}")

    return json_data


def get__ac_signature(one_time_stamp, one_site, one_nonce, ua_n):
    def cal_one_str(one_str, orgi_iv):
        k = orgi_iv
        for char in one_str:
            a = ord(char)
            k = ((k ^ a) * 65599) & 0xFFFFFFFF
        return k

    def cal_one_str_3(one_str, orgi_iv):
        k = orgi_iv
        for char in one_str:
            k = (k * 65599 + ord(char)) & 0xFFFFFFFF
        return k

    def get_one_chr(enc_chr_code):
        if enc_chr_code < 26:
            return chr(enc_chr_code + 65)
        elif enc_chr_code < 52:
            return chr(enc_chr_code + 71)
        elif enc_chr_code < 62:
            return chr(enc_chr_code - 4)
        else:
            return chr(enc_chr_code - 17)

    def enc_num_to_str(one_orgi_enc):
        s = ''
        for i in range(24, -1, -6):
            s += get_one_chr((one_orgi_enc >> i) & 63)
        return s

    sign_head = '_02B4Z6wo00f01'
    time_stamp_s = str(one_time_stamp)

    a = cal_one_str(one_site, cal_one_str(time_stamp_s, 0)) % 65521
    b = int("10000000110000" + bin((one_time_stamp ^ (a * 65521)) & 0xFFFFFFFF)[2:].zfill(32), 2)
    b_s = str(b)
    c = cal_one_str(b_s, 0)
    d = enc_num_to_str(b >> 2)
    e = (b // 4294967296) & 0xFFFFFFFF
    f = enc_num_to_str((b << 28) | (e >> 4))
    g = 582085784 ^ b
    h = enc_num_to_str((e << 26) | (g >> 6))
    i = get_one_chr(g & 63)
    j = ((cal_one_str(ua_n, c) % 65521) << 16) | (cal_one_str(one_nonce, c) % 65521)
    k = enc_num_to_str(j >> 2)
    l = enc_num_to_str((j << 28) | ((524576 ^ b) >> 4))
    m = enc_num_to_str(a)
    n = sign_head + d + f + h + i + k + l + m
    o = format(cal_one_str_3(n, 0) & 0xFF, '02x')
    signature = n + o
    return signature


import time
import requests


def _cal_one_str(s: str, iv: int) -> int:
    """等价 JS 的 cal_one_str"""
    k = iv
    for ch in s:
        k = ((k ^ ord(ch)) * 65599) & 0xFFFFFFFF
    return k


def _cal_one_str_2(s: str, iv: int) -> int:
    """等价 JS 的 cal_one_str_2"""
    k, a = iv, len(s)
    for i in range(32):
        k = (k * 65599 + ord(s[k % a])) & 0xFFFFFFFF
    return k


def _cal_one_str_3(s: str, iv: int) -> int:
    """等价 JS 的 cal_one_str_3"""
    k = iv
    for ch in s:
        k = (k * 65599 + ord(ch)) & 0xFFFFFFFF
    return k


def _get_one_chr(code: int) -> str:
    """等价 JS 的 get_one_chr"""
    if code < 26:
        return chr(code + 65)
    if code < 52:
        return chr(code + 71)
    if code < 62:
        return chr(code - 4)
    return chr(code - 17)


def _enc_num_to_str(v: int) -> str:
    """等价 JS 的 enc_num_to_str"""
    s = ""
    for i in range(24, -1, -6):
        s += _get_one_chr((v >> i) & 63)
    return s


def __ac_signature(timestamp: int, site: str, nonce: str, ua: str) -> str:
    """
    timestamp : int   秒级时间戳（如 1740635781）
    site      : str   当前页面 host+path，如 'www.douyin.com/'
    nonce     : str   服务端下发的 __ac_nonce
    ua        : str   完整 User-Agent
    return    : str   __ac_signature
    """
    sign_head = "_02B4Z6wo00f01"
    ts_str = str(timestamp)

    # 步骤与 JS 完全对应
    a = _cal_one_str(site, _cal_one_str(ts_str, 0)) % 65521
    b = int("10000000110000" + format((timestamp ^ (a * 65521)) & 0xFFFFFFFF, "032b"), 2)
    b_str = str(b)
    c = _cal_one_str(b_str, 0)
    d = _enc_num_to_str(b >> 2)
    e = (b // 4294967296) & 0xFFFFFFFF
    f = _enc_num_to_str((b << 28) | (e >> 4))
    g = 582085784 ^ b
    h = _enc_num_to_str((e << 26) | (g >> 6))
    i = _get_one_chr(g & 63)
    j = ((_cal_one_str(ua, c) % 65521) << 16) | (_cal_one_str(nonce, c) % 65521)
    k = _enc_num_to_str(j >> 2)
    l = _enc_num_to_str((j << 28) | ((524576 ^ b) >> 4))
    m = _enc_num_to_str(a)
    n = sign_head + d + f + h + i + k + l + m
    o = format(_cal_one_str_3(n, 0) & 0xFF, "02x")[-2:]
    return n + o


def get_ms_token(randomlength=107):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def get_mstoken():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'text/plain; text/plain;charset=UTF-8',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.douyin.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.douyin.com/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
    }

    params = {
        'ms_appid': '6383',
    }

    data = '{"magic":538969122,"version":1,"dataType":8,"strData":"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","tspFromClient":1757956573349,"ulr":0}'

    response = requests.post('https://mssdk.bytedance.com/web/r/token', params=params, headers=headers, data=data)
    return response.cookies.get_dict()["msToken"]


def gen_secsdk_uid() -> str:
    """
    生成与抖音 Web 端安全 SDK 完全一致的 x-web-secsdk-uid
    返回 36 位标准 v4 UUID 字符串（带横杠）
    """
    # 1. 生成 16 字节随机数
    raw = bytearray(16)
    for i in range(16):
        if i & 3 == 0:  # 每 4 字节重新取一次随机数
            chunk = random.getrandbits(32)
        raw[i] = (chunk >> ((i & 3) << 3)) & 0xff

    # 2. 设置 version=4（高 4 位=0b0100）
    raw[6] = (raw[6] & 0x0f) | 0x40
    # 3. 设置 variant=10x（高 2 位=0b10）
    raw[8] = (raw[8] & 0x3f) | 0x80

    # 4. 格式化成 8-4-4-4-12
    hex_str = raw.hex()
    return '{}-{}-{}-{}-{}'.format(
        hex_str[0:8],
        hex_str[8:12],
        hex_str[12:16],
        hex_str[16:20],
        hex_str[20:32]
    )


async def get_douyin_cookies(proxy):
    url = "https://www.douyin.com/"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform': '"Windows"',
        'x-secsdk-csrf-token': 'DOWNGRADE',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.douyin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.douyin.com/?recommend=1',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
    }
    async with httpx.AsyncClient(proxy=proxy) as client:
        client.headers = headers
        await client.get(url, follow_redirects=False)
        __ac_nonce = client.cookies.get("__ac_nonce")
        sig = __ac_signature(int(time.time()), url, __ac_nonce, user_agent)
        client.cookies.update({
            "__ac_nonce": __ac_nonce,
            "__ac_signature": sig,
            "__ac_referer": "__ac_blank"
        })
        await client.get(url, follow_redirects=False)
        client.cookies.update({"x-web-secsdk-uid": gen_secsdk_uid()})
        url = "https://www.douyin.com/report/pc_web_crash"
        data = [
            {
                "age": 0,
                "body": {
                    "columnNumber": 32019,
                    "id": "UnloadHandler",
                    "lineNumber": 1,
                    "message": "Unload event listeners are deprecated and will be removed.",
                    "sourceFile": "https://lf3-cdn-tos.bytescm.com/obj/static/log-sdk/collect/5.1/collect.zip.js"
                },
                "type": "deprecation",
                "url": "https://www.douyin.com/",
                "user_agent": user_agent
            }
        ]
        response = await client.post(url, json=data)
        uifid = client.cookies.get("UIFID_TEMP")
        json_data = {
            'aid': 6383,
            'service': 'www.douyin.com',
        }
        response = await client.post('https://www.douyin.com/ttwid/check/', headers=headers, json=json_data)
        cookie = "; ".join([f"{c.name}={c.value}" for c in client.cookies.jar])
        return cookie

# asyncio.run(get_douyin_cookies(proxy=None))


# asyncio.run(get_douyin_cookies("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36", None))



async def process_data_in_js(url, data="", userAgent=""):
    async with aiofiles.open('application/src/douyin/args/longab.js', 'r', encoding='utf-8') as file:
        js_code = await file.read()

    ctx = execjs.compile(js_code)
    return ctx.call('getABogus', *(url, data, userAgent))