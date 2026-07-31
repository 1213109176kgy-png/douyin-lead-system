#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：parameter.py
@IDE     ：PyCharm 

@Date    ：2025/4/18 20:54 
'''
URL_PATH = {
    "billboard_category": "/v1/billboard/distribution",
    "up_hot": "/v1/billboard/rise",
    "city_value": "/v1/common/city",
    "city_billboard": "/v1/billboard/city",
    "challenge_billboard": "/v1/billboard/challenge",
    "total_billboard": "/v1/billboard/total",
    "sentence_video": "/v1/sentence/",
    "user_fans_data": "/v1/author_analysis/user_portrait",
    "user_fans_interest": "/v1/author_analysis/",
    "aweme_digs_data": "/v1/item_analysis/",
    "hot_spot_video": "/v1/material/video_billboard",
    "product_data": "/v1/author_analysis/product_analysis/product_data",
    "monitor_user": "/v1/monitor/user/query_list",
    "hot_spot_category": "/v1/material/content_tag?sort_key=category_priority"
}

DOUYIN_BILLBOARD_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}
