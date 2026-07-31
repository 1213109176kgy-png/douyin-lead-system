# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：core.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 13:57 
@WebSite ：
'''
import codecs
import json
import re

from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from core import json_success_response, CustomException
from libs.request import get_request_data



async def get_visitor_data(app, video_id, proxy):
    url = "https://www.youtube.com/youtubei/v1/player?prettyPrint=false"
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "osName": "Windows",
                "osVersion": "10.0",
                "clientVersion": "2.20250122.01.00",
                "platform": "DESKTOP"
            }
        },
        "videoId": video_id,
        "contentCheckOk": "true"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Youtube-Client-Name': '1',
        'X-Youtube-Client-Version': '2.20250122.01.00',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'www.youtube.com',
        'Connection': 'keep-alive'
    }
    response = await app.ctx.curl_client.http_post(url=url, headers=headers,json=payload, proxy=proxy, requests_client="httpx")
    return response.json()['responseContext']['visitorData']


async def get_video_data(app, video_id, proxy):
    visitor_data = await get_visitor_data(app, video_id, proxy)
    url = "https://www.youtube.com/youtubei/v1/player?prettyPrint=false"

    payload = {
        "context": {
            "client": {
                "clientName": "ANDROID_VR",
                "clientVersion": "1.60.19",
                "deviceMake": "Oculus",
                "deviceModel": "Quest 3",
                "osName": "Android",
                "osVersion": "12L",
                "androidSdkVersion": "32",
                "visitorData": visitor_data
            }
        },
        "videoId": video_id,
        "contentCheckOk": "true"
    }
    headers = {
        'User-Agent': 'com.google.android.apps.youtube.vr.oculus/1.60.19 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip',
        'X-Youtube-Client-Name': '28',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'www.youtube.com',
        'Connection': 'keep-alive',
    }

    response = await app.ctx.curl_client.http_post(url=url, headers=headers, json=payload, proxy=proxy, requests_client="httpx")

    return response.json()



async def get_user_channel_id(app, username, proxy):
    url = f"https://www.youtube.com/@{username}/featured"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'www.youtube.com',
        'Connection': 'keep-alive'
    }
    response = await app.ctx.curl_client.http_get(url=url, headers=headers, proxy=proxy,
                                                   requests_client="httpx")

    text = response.text
    pattern = r'<meta\s+itemprop="identifier"\s+content="([^"]+)"'
    match = re.search(pattern, text)
    if match:
        content_value = match.group(1)
        return content_value
    else:
        raise CustomException(message="获取channel_id失败")


async def get_user_post_first_page(app, url, headers, proxy):
    response = await app.ctx.curl_client.http_get(url=url, headers=headers, proxy=proxy,
                                                  requests_client="httpx", allow_redirects=True)
    try:
        pattern = r"var ytInitialData = (.*?);</script><script"
        match = re.search(pattern, response.text, re.DOTALL)

        yt_initial_data_json = match.group(1)
        return json.loads(yt_initial_data_json)
    except Exception as e:
        raise CustomException(message="获取失败")


async def get_user_post_next_page(app, url, headers, payload, proxy):
    response = await app.ctx.curl_client.http_post(url=url, headers=headers,json=payload, proxy=proxy,
                                                  requests_client="httpx")
    return response.json()




class BaseYouTubeView(HTTPMethodView):
    """
    基础YouTube视图类
    """

    URL = ""
    REQUIRED_KEYS = []
    DEFAULT_VALUES = {}

    async def get_params(self, request: Request) -> dict:
        data = await get_request_data(request)
        params = {key: data.get(key, self.DEFAULT_VALUES.get(key)) for key in self.DEFAULT_VALUES}
        missing_keys = [key for key in self.REQUIRED_KEYS if not params.get(key)]
        if missing_keys:
            raise CustomException()

        params['key'] = data.get('key') or request.app.config.get("GOOGLE_API_KEY") or None

        return params

    async def post(self, request: Request) -> HTTPResponse:
        params = await self.get_params(request)
        if not params['key']:
            raise CustomException(message="请填写配置文件的APIKey")
        if not params:
            raise CustomException()
        response = await request.app.ctx.curl_client.http_get(url=f"https://youtube.googleapis.com/youtube/v3/{self.URL}", params=params, requests_client="httpx")
        return json_success_response(response.json())


