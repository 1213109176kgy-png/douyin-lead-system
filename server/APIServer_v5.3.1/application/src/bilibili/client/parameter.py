#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：parameter.py
@IDE     ：PyCharm 

@Date    ：2025/4/21 9:49 
'''
from bilibili_api import search

BASE_PC_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.bilibili.com',
    'Connection': 'keep-alive',
    'Referer': f'https://www.bilibili.com/'
}

BASE_MOBILE_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/131.0.0.0',
    'Host': 'api.bilibili.com',
    'Connection': 'keep-alive',
}

search_type_map = {
    "VIDEO": search.SearchObjectType.VIDEO,
    "BANGUMI": search.SearchObjectType.BANGUMI,
    "FT": search.SearchObjectType.FT,
    "LIVE": search.SearchObjectType.LIVE,
    "ARTICLE": search.SearchObjectType.ARTICLE,
    "TOPIC": search.SearchObjectType.TOPIC,
    "USER": search.SearchObjectType.USER,
    "LIVEUSER": search.SearchObjectType.LIVEUSER,
}

order_type_map = {
    "VIDEO": {
        "CLICK": search.OrderVideo.CLICK,
        "PUBDATE": search.OrderVideo.PUBDATE,
        "DM": search.OrderVideo.DM,
        "STOW": search.OrderVideo.STOW,
        "SCORES": search.OrderVideo.SCORES,
        "DEFAULT": search.OrderVideo.TOTALRANK
    },
    "LIVE": {
        "NEWLIVE": search.OrderLiveRoom.NEWLIVE,
        "ONLINE": search.OrderLiveRoom.ONLINE,
        "DEFAULT": search.OrderLiveRoom.ONLINE
    },
    "ARTICLE": {
        'CLICK': search.OrderArticle.CLICK,
        'PUBDATE': search.OrderArticle.PUBDATE,
        'ATTENTION': search.OrderArticle.ATTENTION,
        'SCORES': search.OrderArticle.SCORES,
        'DEFAULT': search.OrderArticle.TOTALRANK
    },
    "USER": {
        "FANS": search.OrderUser.FANS,
        "LEVEL": search.OrderUser.LEVEL,
        "DEFAULT": search.OrderUser.LEVEL
    }
}
