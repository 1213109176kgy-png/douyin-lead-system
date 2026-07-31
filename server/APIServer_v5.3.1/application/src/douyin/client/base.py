#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：base.py
@IDE     ：PyCharm 

@Date    ：2025/4/15 21:26 
'''
import json
import random
import re
from typing import List, Optional, Dict
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
from sanic import Request

from application.src.douyin.args.abogus import ABogus
from application.src.douyin.args.abogus_old import encrypt_abogus
from application.src.douyin.args.common import generate_ttwid
from application.src.douyin.args.x_gorgons import X_Gorgon0404
from application.src.douyin.args.xb import XBogus
from application.src.douyin.client.parameter import ITEM_ID_PATTERNS, PC_HEADERS, APP_HEADERS, MOBILE_HEADERS, PC_UA, \
    params_v2_path
from core import CustomException, get_device_data
from libs import get_request_data, get_request_proxy
from libs.common import extract_url, generate_random_string_alph, get_domain_from_url


class RequestValidator:
    def __init__(self, required_params: List[str], one_of_required_params: List[str],
                 optional_params: Dict[str, Optional[str]]):
        self.required_params = required_params
        self.one_of_required_params = one_of_required_params
        self.optional_params = optional_params

    async def validate(self, request: Request):
        data = await get_request_data(request)
        main_id = None
        for param in self.required_params:
            param_value = data.get(param, "").strip()
            if not param_value:
                raise CustomException(f"必填参数 '{param}' 不能为空")
            main_id = param_value
        main_id = main_id if main_id else data.get(self.one_of_required_params[0])  # 优先使用第一个参数
        if not main_id and data.get("share_text"):
            main_id = await self.get_item_id(data["share_text"], request)
        if not main_id:
            raise CustomException(f"至少提供以下参数之一: {', '.join(self.one_of_required_params)}")
        validated_data = {param: data.get(param, default) for param, default in self.optional_params.items()}
        validated_data.update(data)
        validated_data["main_id"] = main_id

        return validated_data

    @staticmethod
    async def get_item_id(share_text: str, request):
        """
        获取ID
        """
        link = await extract_url(share_text)
        if not link:
            return None

        url = link
        patterns = ITEM_ID_PATTERNS
        proxy = await get_request_proxy(request)
        response = await request.app.ctx.curl_client.http_get(url=url, headers=PC_HEADERS, proxy=proxy)
        response_url = response.headers.get('Location') or str(response.url)
        parsed_url = urlparse(response_url)
        query_params = parse_qs(parsed_url.query)
        sec_uid = query_params.get("sec_uid", [None])[0]
        if sec_uid:
            return sec_uid
        for key, pattern in patterns.items():
            if key in response_url:
                match = re.search(pattern, response_url)
                if match.group(1):
                    return match.group(1)
                if match.group(2):
                    return match.group(2)

        return None


class DouyinClient(object):
    def __init__(self, request):
        self.request = request
        self.pc_domain = 'https://www.douyin.com'
        self.app_domain = "https://aweme.snssdk.com"
        self.search_domain = "https://search3-search.amemv.com"

    async def _get_device_data(self, device_type: str = 'general') -> dict:
        try:
            device_data = await get_device_data(self.request.app, device_type=device_type)
            return device_data
        except Exception as e:
            raise

    @staticmethod
    async def _app_cookie(device_data, sessionid=None):
        data = (f"sessionid={await generate_random_string_alph(32) if not sessionid else sessionid};store-region=cn-ah;"
                f"store-region-src=did; install_id={device_data['install_id_str']}; "
                f"ttreq=1${await generate_random_string_alph(40)}; odin_tt={await generate_random_string_alph(160)}")
        return data

    @staticmethod
    async def _app_header(params_str: str, cookies: str = '', host: str = '') -> dict:
        if cookies is None:
            cookies = ""
        xgorgon = X_Gorgon0404(params_str, '', cookies)
        headers = APP_HEADERS.copy()
        headers.update({
            'X-Gorgon': xgorgon.get('X-Gorgon'),
            'X-Khronos': xgorgon.get('X-Khronos'),
            'Cookie': cookies,
            'Host': await get_domain_from_url(host) if host else "aweme.snssdk.com",
        })
        return headers


    async def _search_headers(self):
        headers = {
            "User-Agent": "AwemeLite 32.9.0 rv:329009 (iPad; iPadOS 16.1.1; zh_CN) Cronet",
            "Accept-Encoding": "gzip, deflate",
            "x-vc-bdturing-sdk-version": "3.7.2",
            "sdk-version": "2",
            "passport-sdk-version": "6.0.0-alpha.55",
            "x-tt-request-tag": "s=-1",
            "x-ss-dp": "2329",
        }
        return headers

    async def _search_encrypt_data(self,url, params,device_data):
        headers = await self._search_headers()
        params_v2 = await params_v2_path()
        device_token = device_data['device_token']
        device_id = device_data['device_id_str']
        sign_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "device_token": device_token,
            "device_id": device_id,
            "x_common_params_v2": params_v2,
            "data": {}
        }
        get_encrypt = await self.request.app.ctx.curl_client.aweme_encrypt_data_v2(sign_data)
        url = get_encrypt['data']["url"]
        headers = get_encrypt['data']["header"]
        headers["x-common-params-v2"] = params_v2
        return url, headers


    async def _pc_header(self, cookies: str = '', agent: str = '', referer: str = "") -> dict:
        headers = PC_HEADERS.copy()
        cookie = cookies if cookies else f"ttwid={await generate_ttwid(self.request)};stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22;IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22;FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D;SEARCH_RESULT_LIST_TYPE=%22single%22;device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64;"
        agent = agent if agent else headers['User-Agent']
        headers.update({
            "Cookie": cookie,
            "User-Agent": agent
        })
        if referer:
            headers.update({"Referer": referer})
        return headers

    @staticmethod
    async def _mobile_header():
        headers = MOBILE_HEADERS.copy()
        return headers

    async def _http_request(self, url: str, headers: dict, params: dict = None, data: [dict, str] = None, json:[dict, str] = None,
                            allow_redirects: bool = True, request_method: str = "GET", proxy=None):
        proxy = None if proxy is False else await get_request_proxy(self.request)
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

    async def parse_aweme_detail_html(self, res_text):
        soup = BeautifulSoup(res_text, 'lxml')
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'videoInfoRes' in script.string:
                script_content = script.string
                # 提取"videoInfoRes"的值
                match = re.search(r'"videoInfoRes":\s*({.*?})\s*}', script_content, re.DOTALL)
                if match:
                    video_info_res = match.group(1)
                    # 由于videoInfoRes是一个JSON对象，需要找到完整的JSON对象结尾
                    brace_count = 0
                    start_index = script_content.find('"videoInfoRes":') + len('"videoInfoRes":')
                    for i, char in enumerate(script_content[start_index:], start=start_index):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                        if brace_count == 0:
                            end_index = i
                            break
                    video_info_res = script_content[start_index:end_index + 1]
                    data = json.loads(video_info_res)['item_list'][0]
                    return data
        else:
            return None

    async def parse_live_info(self, res_text):
        pattern = r'self\.__rsc_f\.push\(\[.*?\]\)'
        matches = re.findall(pattern, res_text)

        if matches:
            last_match = matches[-1]
            data = last_match.replace('self.__rsc_f.push([1,"5:[\\"$\\",\\"$L7\\",null,', "").replace(']\\n"])',
                                                                                                      "").replace('\\"',
                                                                                                                  '"').replace(
                '\\"', '"')
            data = json.loads(data)
            return data
        return None

    async def process_a_bogus(self, params):
        ab = ABogus()
        a_bogus = await ab.get_value(params)
        return f"{params}&a_bogus={a_bogus}"

    async def process_a_bogus_old(self, user_agent=None, params: str = "", body=""):
        if not user_agent:
            user_agent = PC_UA
        a_bogus = await encrypt_abogus(user_agent=user_agent, query=params, body=body)
        return f"{params}&a_bogus={a_bogus}"

    async def process_x_bogus(self, params):
        xb = XBogus()
        x_bogus = await xb.getXBogus(params)
        return x_bogus

    async def get_web_id(self, user_agent, url="https://www.douyin.com", proxy=None):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': url,
            'User-Agent': user_agent
        }

        app_id = 6383
        body = {
            "app_id": app_id,
            "referer": url,
            "url": url,
            "user_agent": user_agent,
            "user_unique_id": ''
        }

        request_url = f"https://mcs.zijieapi.com/webid?aid={app_id}&sdk_version=5.1.18_zip&device_platform=web"
        response = await self._http_request(request_url, headers=headers, data=json.dumps(body), proxy=proxy,
                                            request_method="POST")
        jsonObj = json.loads(response.text)
        return jsonObj['web_id']

    def get_ms_token(self, randomlength=107):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str
