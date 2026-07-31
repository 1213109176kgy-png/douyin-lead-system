#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：search.py
@IDE     ：PyCharm 

@Date    ：2025/9/24 13:48 
'''
import json
import os
import re
import subprocess
import time

import httpx


def get_signature(time_stamp10, href_site, nonce, ua_n):
    """
    通过 Node 执行压缩后的 JS 拿到 __ac_signature
    """

    def do_one_cmd(one_cmd):
        result = subprocess.run(one_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding='utf-8')
        return {'returncode': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr}

    def do_one_js_code(js_code_n):
        now_dir = os.path.dirname(os.path.realpath(__file__))
        js_path = os.path.join(now_dir, 'js_code.js')
        with open(js_path, 'w', encoding='utf-8') as js_file:
            js_file.write(js_code_n)
        result = do_one_cmd(f'node {js_path}')  # 确保node在环境变量中。
        os.remove(js_path)
        return result

    js_code_n = r'function get__ac_signature(r,t,n,o){function e(r,t){for(var n=t,o=0;o<r.length;o++)n=65599*(n^r.charCodeAt(o))>>>0;return n}function a(r){return r<26?String.fromCharCode(r+65):r<52?String.fromCharCode(r+71):r<62?String.fromCharCode(r-4):String.fromCharCode(r-17)}function f(r){for(var t="",n=24;0<=n;n-=6)t+=a(r>>n&63);return t}var t=e(t,e(r+"",0))%65521,i=e((r=parseInt("10000000110000"+parseInt((r^65521*t)>>>0).toString(2).padStart(32,"0"),2))+"",0),u=r/4294967296>>>0,g=582085784^r;return(n="_02B4Z6wo00f01"+f(r>>2)+f(r<<28|u>>>4)+f(u<<26|g>>>6)+a(63&g)+f((o=e(o,i)%65521<<16|e(n,i)%65521)>>2)+f(o<<28|(524576^r)>>>4)+f(t))+parseInt(function(r){for(var t=0,n=0;n<r.length;n++)t=65599*t+r.charCodeAt(n)>>>0;return t}(n)).toString(16).slice(-2)}'  # 压缩后的get__ac_signature函数
    js_code_n += f'console.log(get__ac_signature({time_stamp10},"{href_site}","{nonce}","{ua_n}"))'
    return do_one_js_code(js_code_n)['stdout']


def build_headers(user_agent: str, url: str = "https://www.douyin.com") -> dict:
    """
    根据传入的 UA 和目标 URL，自动生成一套常用的 HTTP 请求头
    :param user_agent: 浏览器 User-Agent 字符串
    :param url: 目标链接（用于提取 referer 域名），默认抖音首页
    :return: 可直接传给 requests / httpx 的 headers 字典
    """
    ua = user_agent.strip()

    # 判断是否为移动端
    is_mobile = "Mobile" in ua

    # 提取平台信息（括号内第一段）
    platform = ""
    if m := re.search(r"\([^;)]+", ua):
        platform = m.group(0)[1:]  # 去掉左括号

    # 识别浏览器及主版本号
    browser, version = "Unknown", "130"
    if "Edg" in ua or "Edge" in ua:
        browser = "Microsoft Edge"
        if m := re.search(r"(?:Edg|Edge)/([\d.]+)", ua):
            version = m.group(1)
    elif "Chrome" in ua:
        browser = "Chromium"
        if m := re.search(r"Chrome/([\d.]+)", ua):
            version = m.group(1)
    elif "Firefox" in ua:
        browser = "Firefox"
        if m := re.search(r"Firefox/([\d.]+)", ua):
            version = m.group(1)
    elif "Safari" in ua and "Chrome" not in ua:
        browser = "Safari"
        if m := re.search(r"Version/([\d.]+)", ua):
            version = m.group(1)

    # 构造 Sec-CH-UA 客户端提示
    sec_ch_ua = f'"{browser}";v="{version.split(".")[0]}", "Not)A;Brand";v="99"'

    # 用域名拼 referer
    host = url.split("/")[2] if "://" in url else url
    referer = f"https://{host}/"

    headers = {
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": referer,
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": "?1" if is_mobile else "?0",
        "sec-ch-ua-platform": f'"{platform}"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": ua,
    }
    return headers


def get_cookies(ua: str = None, proxy: str = None):
    """
    先拿一次首页拿 nonce，再算 signature，再补一次请求，返回最终 Cookie 字典
    """
    ua = ua or (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )
    headers_n = build_headers(ua)
    session = httpx.Client(proxy=proxy)
    session.get('https://www.douyin.com/', headers=headers_n)
    cookies_n = dict(session.cookies)

    signature = get_signature(int(time.time()), 'www.douyin.com/', cookies_n['__ac_nonce'], headers_n['user-agent'])
    session.cookies.set('__ac_signature', signature)

    session.head('https://www.douyin.com/', headers=headers_n)
    cookies_n = dict(session.cookies)
    return cookies_n


class Search():
    def __init__(self, proxy, cookie=None):
        self.session = httpx.Client(proxy=proxy)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        self.session.headers.update(build_headers(self.user_agent))
        if cookie:
            self.session.headers['Cookie'] = cookie
        else:
            self.session.cookies.update(get_cookies(self.user_agent, proxy))
        self.uifid = None
        self.search_id = ""
        if not cookie:
            self.ttwid_check()

    def ttwid_check(self):
        headers = {
            'User-Agent': self.user_agent,
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
        json_data = {
            'aid': 6383,
            'service': 'www.douyin.com',
        }
        self.session.post('https://www.douyin.com/ttwid/check/', headers=headers, json=json_data)

    def search_stream(self, keyword, count, publish_time, content_type, filter_duration, sort_type, search_range):
        url = "https://www.douyin.com/aweme/v1/web/general/search/stream/"
        params = {
            "aid": "6383",
            "browser_language": "zh-CN",
            "browser_name": "Chrome",
            "browser_online": "true",
            "browser_platform": "Win32",
            "browser_version": "140.0.0.0",
            "channel": "channel_pc_web",
            "cookie_enabled": "true",
            "count": count,
            "cpu_core_num": "20",
            "device_memory": "8",
            "device_platform": "webapp",
            "disable_rs": "1",
            "downlink": "1.3",
            "effective_type": "3g",
            "enable_history": "1",
            "engine_name": "Blink",
            "engine_version": "140.0.0.0",
            # "from_group_id": "7548473839907294483",
            "is_filter_search": "0",
            "keyword": keyword,
            "list_type": "",
            "need_filter_settings": "1",
            "offset": "0",
            "os_name": "Windows",
            "os_version": "10",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "platform": "PC",
            "query_correct_type": "1",
            "round_trip_time": "400",
            "screen_height": "1440",
            "screen_width": "2560",
            "search_channel": "aweme_general",
            "search_source": "normal_search",
            "support_dash": "0",
            "support_h265": "1",
            "uifid": self.uifid,
            "version_code": "190600",
            "version_name": "19.6.0",
        }
        if not sort_type == '0' or not publish_time == "0" or not filter_duration == "" or not content_type == "0":
            params.update({
                "is_filter_search": "1",
                "filter_selected": f'{{"sort_type":"{sort_type}","publish_time":"{publish_time}","filter_duration":"{filter_duration}","content_type":"{content_type}, "search_range":"{search_range}"}}'
            })

        response = self.session.get(url, params=params)
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
                self.search_id = obj.get("extra").get("logid")
                print(self.search_id)
                return obj
                # 或者 print(obj)  # 已转好的字典

    def search_single(self, keyword, count, offset, publish_time, content_type, filter_duration, sort_type,search_range, search_id):
        url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": "aweme_general",
            "enable_history": "1",
            "keyword": keyword,
            "search_source": "normal_search",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "from_group_id": "",
            "disable_rs": "1",
            "offset": offset,
            "count": count,
            "need_filter_settings": "0",
            "list_type": "",
            "update_version_code": "170400",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "support_h265": "1",
            "support_dash": "1",
            "cpu_core_num": "20",
            "version_code": "190600",
            "version_name": "19.6.0",
            "cookie_enabled": "true",
            "screen_width": "2560",
            "screen_height": "1440",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "140.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "140.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "1.3",
            "effective_type": "3g",
            "round_trip_time": "400",
            "search_id": search_id,
        }
        if not sort_type == '0' or not publish_time == "0" or not filter_duration == "" or not content_type == "0" or search_range == "0":
            params.update({
                "is_filter_search": "1",
                "filter_selected": f'{{"sort_type":"{sort_type}","publish_time":"{publish_time}","filter_duration":"{filter_duration}","content_type":"{content_type}","search_range":"{search_range}"}}'
            })

        response = self.session.get(url, params=params)
        return response.json()

    def search_item(self, keyword, count, offset, publish_time, filter_duration, sort_type,search_range, search_id):
        url = "https://www.douyin.com/aweme/v1/web/search/item/"
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": "aweme_video_web",
            "enable_history": "1",
            "keyword": keyword,
            "search_source": "normal_search",
            "query_correct_type": "1",
            "is_filter_search": "0",
            "from_group_id": "",
            "disable_rs": "1",
            "offset": offset,
            "count": count,
            "need_filter_settings": "1",
            "list_type": "single",
            "update_version_code": "170400",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "support_h265": "1",
            "support_dash": "1",
            "cpu_core_num": "20",
            "version_code": "170400",
            "version_name": "17.4.0",
            "cookie_enabled": "true",
            "screen_width": "2560",
            "screen_height": "1440",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Chrome",
            "browser_version": "140.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "140.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "1.3",
            "effective_type": "3g",
            "round_trip_time": "400",
            "search_id": search_id
        }

        if not sort_type == '0' or not publish_time == "0" or not filter_duration == "" or not sort_type=="0":
            params.update({
                "is_filter_search": "1",
                "sort_type": sort_type,
                "publish_time": publish_time,
                "filter_duration": filter_duration,
                "search_range": search_range,
            })

        response = self.session.get(url, params=params)
        return response.json()





import time

from curl_cffi import requests


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


async def get_cookie(headers, proxy=None):
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

