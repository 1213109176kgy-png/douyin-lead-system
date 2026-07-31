# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：views.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 13:53 
@WebSite ：
'''
import re

from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.youtube.client.client import BaseYouTubeView, get_video_data, get_user_channel_id, \
    get_user_post_first_page, get_user_post_next_page
from core import json_success_response, CustomException
from libs.request import get_request_data, get_request_proxy


class AwemeDetailView(HTTPMethodView):
    """
    单一视频
    """

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        video_id = data.get("video_id", None)
        proxy = await get_request_proxy(request, proxy_type="overseas")
        response = await get_video_data(app=request.app, video_id=video_id, proxy=proxy)
        return json_success_response(response)


class VideoCommentView(BaseYouTubeView):
    """
    视频评论
    """
    URL = "commentThreads"
    REQUIRED_KEYS = ["video_id"]
    DEFAULT_VALUES = {
        "key": None,
        "video_id": None,
        "max_results": "40",
        "order": "time",
        "page_token": "",
        "part": "id,snippet,replies"
    }


class SearchDataView(BaseYouTubeView):
    """
    搜索数据
    """
    URL = "search"
    REQUIRED_KEYS = ["q"]
    DEFAULT_VALUES = {
        "key": None,
        "q": None,
        "max_results": "40",
        "order": "relevance",
        "page_token": "",
        "type": "video",
        "region_code": "",
        "part": "snippet"
    }


class PlaylistsView(BaseYouTubeView):
    """
    播放列表
    """
    URL = "playlists"
    REQUIRED_KEYS = ["channel_id"]
    DEFAULT_VALUES = {
        "key": None,
        "channel_id": None,
        "max_results": "40",
        "page_token": "",
        "part": "snippet,contentDetails,localizations,player,status,id"
    }


class PlaylistItemsView(BaseYouTubeView):
    """
    视频列表
    """
    URL = "playlistItems"
    REQUIRED_KEYS = ["playlist_id"]
    DEFAULT_VALUES = {
        "key": None,
        "playlist_id": None,
        "max_results": "40",
        "page_token": "",
        "part": "snippet,status,id,contentDetails"
    }


class GetChannelIDView(HTTPMethodView):
    """
    获取用户的channelID
    """

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        username = data.get("username", None)
        proxy = await get_request_proxy(request, proxy_type="overseas")
        response = await get_user_channel_id(app=request.app, username=username, proxy=proxy)
        return json_success_response(response)


class UserPostView(HTTPMethodView):
    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        username = data.get("username") or None
        user_url = data.get("user_url") or None
        post_type = data.get("post_type") or "videos"
        continuation = data.get("continuation") or ""
        proxy = await get_request_proxy(request, proxy_type="overseas")
        if not username:
            if not user_url:
                raise CustomException(message="参数错误")
            pattern = r'@([^/]+)'
            match = re.search(pattern, user_url)
            try:
                username = match.group(1)
            except Exception as e:
                raise CustomException(message="参数错误")

        headers = {
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua-arch': '"arm"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Chromium";v="134.0.6998.45", "Not:A-Brand";v="24.0.0.0", "Microsoft Edge";v="134.0.3124.51"',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform-version': '"15.2.0"',
            'sec-ch-ua-wow64': '?0',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': 'www.youtube.com',
            'Connection': 'keep-alive'
        }
        if not continuation or continuation == "":
            url = f"https://www.youtube.com/@{username}/{post_type}?app=desktop&sttick=1"
            response = await get_user_post_first_page(app=request.app, url=url, headers=headers, proxy=proxy)
            return json_success_response(response)
        url = "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false"
        payload = {
            "context": {
                "client": {
                    "hl": "zh-CN",
                    "gl": "HK",
                    "deviceMake": "Apple",
                    "deviceModel": "",
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20250905.01.00",
                    "osName": "Macintosh",
                    "osVersion": "10_15_7",
                    "originalUrl": f"https://www.youtube.com/@{username}/shorts?app=desktop",
                    "screenPixelDensity": 2,
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "screenDensityFloat": 2,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "timeZone": "Asia/Shanghai",
                    "browserName": "Edge Chromium",
                    "browserVersion": "134.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "screenWidthPoints": 623,
                    "screenHeightPoints": 898,
                    "utcOffsetMinutes": 480,
                    "connectionType": "CONN_CELLULAR_4G",
                    "memoryTotalKbytes": "8000000",
                    "mainAppWebInfo": {
                        "graftUrl": f"https://www.youtube.com/@{username}/shorts?app=desktop",
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True
                    }
                },
                "user": {
                    "lockedSafetyMode": False
                },
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": []
                },
            },
            "continuation": continuation
        }
        response = await get_user_post_next_page(app=request.app, url=url, headers=headers, payload=payload,
                                                 proxy=proxy)
        return json_success_response(response)


class CommentListView(HTTPMethodView):
    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        video_id = data.get("video_id") or None
        continuation = data.get("continuation") or ""
        proxy = await get_request_proxy(request, proxy_type="overseas")

        url = "https://www.youtube.com/youtubei/v1/next?prettyPrint=false"
        payload = {
            "context": {
                "client": {
                    "hl": "zh-CN",
                    "gl": "JP",
                    "remoteHost": "",
                    "deviceMake": "",
                    "deviceModel": "",
                    "visitorData": "",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36,gzip(gfe)",
                    "clientName": "WEB",
                    "clientVersion": "2.20251222.04.00",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "originalUrl": f"https://www.youtube.com/watch?v={video_id}",
                    "screenPixelDensity": 2,
                    "platform": "DESKTOP",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "windowWidthPoints": 2552,
                    "configInfo": {
                    },
                    "screenDensityFloat": 1.5,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
                    "timeZone": "Asia/Shanghai",
                    "browserName": "Chrome",
                    "browserVersion": "143.0.0.0",
                    "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "deviceExperimentId": "",
                    "rolloutToken": "",
                    "screenWidthPoints": 1121,
                    "screenHeightPoints": 1274,
                    "utcOffsetMinutes": 480,
                    "memoryTotalKbytes": "8000000",
                    "clientScreen": "WATCH",
                    "mainAppWebInfo": {
                        "graftUrl": f"/watch?v={video_id}",
                        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED",
                        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                        "isWebNativeShareAvailable": True
                    }
                },
                "user": {
                    "lockedSafetyMode": False
                },
                "request": {
                    "useSsl": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": []
                },
                "clickTracking": {
                    "clickTrackingParams": ""
                },
                "adSignalsInfo": {
                    "params": [
                        {
                            "key": "dt",
                            "value": "1766563590812"
                        },
                        {
                            "key": "flash",
                            "value": "0"
                        },
                        {
                            "key": "frm",
                            "value": "0"
                        },
                        {
                            "key": "u_tz",
                            "value": "480"
                        },
                        {
                            "key": "u_his",
                            "value": "4"
                        },
                        {
                            "key": "u_h",
                            "value": "1440"
                        },
                        {
                            "key": "u_w",
                            "value": "2560"
                        },
                        {
                            "key": "u_ah",
                            "value": "1392"
                        },
                        {
                            "key": "u_aw",
                            "value": "2560"
                        },
                        {
                            "key": "u_cd",
                            "value": "24"
                        },
                        {
                            "key": "bc",
                            "value": "31"
                        },
                        {
                            "key": "bih",
                            "value": "1274"
                        },
                        {
                            "key": "biw",
                            "value": "1106"
                        },
                        {
                            "key": "brdim",
                            "value": "0,0,0,0,2560,0,2560,1392,1121,1274"
                        },
                        {
                            "key": "vis",
                            "value": "1"
                        },
                        {
                            "key": "wgl",
                            "value": "true"
                        },
                        {
                            "key": "ca_type",
                            "value": "image"
                        }
                    ]
                }
            },
            "videoId": video_id,
            "racyCheckOk": False,
            "contentCheckOk": False,
            "autonavState": "STATE_NONE",
            "playbackContext": {
                "vis": 0,
                "lactMilliseconds": "-1"
            },
            "captionsRequested": False
        }

        if continuation:
            payload = {
                "context": {
                    "client": {
                        "hl": "zh-CN",
                        "gl": "JP",
                        "remoteHost": "",
                        "deviceMake": "",
                        "deviceModel": "",
                        "visitorData": "",
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20251222.04.00",
                        "osName": "Windows",
                        "osVersion": "10.0",
                        "originalUrl": "https://www.youtube.com/",
                        "platform": "DESKTOP",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "windowWidthPoints": 1121,
                        "configInfo": {

                        },
                        "screenDensityFloat": 1.5,
                        "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
                        "browserName": "Chrome",
                        "browserVersion": "143.0.0.0",
                        "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "deviceExperimentId": "",
                        "rolloutToken": "",
                        "screenWidthPoints": 1121,
                        "screenHeightPoints": 1274,
                        "screenPixelDensity": 2,
                        "utcOffsetMinutes": 480,
                        "connectionType": "CONN_CELLULAR_4G",
                        "memoryTotalKbytes": "8000000",
                        "mainAppWebInfo": {
                            "graftUrl": f"https://www.youtube.com/watch?v={video_id}",
                            "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED",
                            "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                            "isWebNativeShareAvailable": True
                        },
                        "timeZone": "Asia/Shanghai"
                    },
                    "user": {
                        "lockedSafetyMode": False
                    },
                    "request": {
                        "useSsl": True,
                        "internalExperimentFlags": [],
                        "consistencyTokenJars": [
                            {
                                "encryptedTokenJarContents": "",
                                "expirationSeconds": "600"
                            }
                        ]
                    },
                    "clickTracking": {
                        "clickTrackingParams": ""
                    },
                    "adSignalsInfo": {
                        "params": [
                            {
                                "key": "dt",
                                "value": "1766480075491"
                            },
                            {
                                "key": "flash",
                                "value": "0"
                            },
                            {
                                "key": "frm",
                                "value": "0"
                            },
                            {
                                "key": "u_tz",
                                "value": "480"
                            },
                            {
                                "key": "u_his",
                                "value": "20"
                            },
                            {
                                "key": "u_h",
                                "value": "1440"
                            },
                            {
                                "key": "u_w",
                                "value": "2560"
                            },
                            {
                                "key": "u_ah",
                                "value": "1392"
                            },
                            {
                                "key": "u_aw",
                                "value": "2560"
                            },
                            {
                                "key": "u_cd",
                                "value": "24"
                            },
                            {
                                "key": "bc",
                                "value": "31"
                            },
                            {
                                "key": "bih",
                                "value": "1274"
                            },
                            {
                                "key": "biw",
                                "value": "1106"
                            },
                            {
                                "key": "brdim",
                                "value": "0,0,0,0,2560,0,2560,1392,1121,1274"
                            },
                            {
                                "key": "vis",
                                "value": "1"
                            },
                            {
                                "key": "wgl",
                                "value": "true"
                            },
                            {
                                "key": "ca_type",
                                "value": "image"
                            }
                        ]
                    }
                },
                "continuation": continuation
            }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://www.youtube.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": f"https://www.youtube.com/watch?v={video_id}",
            "sec-ch-dpr": "1.5",
            "sec-ch-ua": "\"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"143\"",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-form-factors": "\"Desktop\"",
            "sec-ch-ua-full-version": "\"143.0.7499.147\"",
            "sec-ch-ua-full-version-list": "\"Chromium\";v=\"143.0.7499.147\", \"Not A(Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"143.0.7499.147\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"19.0.0\"",
            "sec-ch-ua-wow64": "?0",
            "sec-ch-viewport-width": "1121",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "same-origin",
            "sec-fetch-site": "same-origin",
            "x-browser-channel": "stable",
            "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
            "x-browser-year": "1969",
            "x-goog-authuser": "0",
            "x-origin": "https://www.youtube.com",
            "x-youtube-bootstrap-logged-in": "true",
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20251222.04.00"
        }

        response = await request.app.ctx.curl_client.http_post(url=url, headers=headers, json=payload, proxy=proxy,
                                                               requests_client="httpx")
        result = response.json()
        if not continuation:
            content = result['contents']['twoColumnWatchNextResults']['results']['results']['contents'][-1]
        else:
            content = result['frameworkUpdates']['entityBatchUpdate']
            content['pages'] = result['onResponseReceivedEndpoints'][-1]
        return json_success_response(content)
