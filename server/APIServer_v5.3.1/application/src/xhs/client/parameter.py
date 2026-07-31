#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：parameter.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 10:07 
'''
import random
from enum import Enum

# 更新浏览器版本号和多样化UA
PC_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

MOBILE_UA_LIST = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.101 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]


def get_random_pc_ua():
    return random.choice(PC_UA_LIST)


def get_random_mobile_ua():
    return random.choice(MOBILE_UA_LIST)


BASE_UA = get_random_pc_ua()
MOBILE_UA = get_random_mobile_ua()

BASE_HEADERS = {
    "User-Agent": BASE_UA,
    "Referer": "https://www.xiaohongshu.com",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

MOBILE_HEADERS = {
    "User-Agent": MOBILE_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}


class SearchSortType(Enum):
    """serach sort type"""

    # 综合
    GENERAL = "general"
    # 最多点赞
    MOST_POPULAR = "popularity_descending"
    # 最新
    LATEST = "time_descending"
    # 最多评论
    COMMENT = "comment_descending"
    # 最多收藏
    COLLECT = "collect_descending"


class SearchNoteTime(Enum):
    """serach notetime type"""

    # 不限
    NO_LIMIT = "不限"
    # 一天内
    ONE_DAY = "一天内"
    # 一周内
    ONE_WEEK = "一周内"
    # 半年内
    HALF_YEAR = "半年内"


class SearchNoteRange(Enum):
    """serach range type"""

    # 不限
    NO_LIMIT = "不限"
    # 已看过
    SEEN = "已看过"
    # 未看过
    NO_SEEN = "未看过"
    # 已关注
    FOLLOWED = "已关注"


class SearchNoteType(Enum):
    """笔记类型"""

    # default
    ALL = "不限"
    # only video
    VIDEO = "视频笔记"
    # only image
    IMAGE = "普通笔记"


class FeedType(Enum):
    # 推荐
    RECOMMEND = "homefeed_recommend"
    # 穿搭
    FASION = "homefeed.fashion_v3"
    # 美食
    FOOD = "homefeed.food_v3"
    # 彩妆
    COSMETICS = "homefeed.cosmetics_v3"
    # 影视
    MOVIE = "homefeed.movie_and_tv_v3"
    # 职场
    CAREER = "homefeed.career_v3"
    # 情感
    EMOTION = "homefeed.love_v3"
    # 家居
    HOURSE = "homefeed.household_product_v3"
    # 游戏
    GAME = "homefeed.gaming_v3"
    # 旅行
    TRAVEL = "homefeed.travel_v3"
    # 健身
    FITNESS = "homefeed.fitness_v3"
