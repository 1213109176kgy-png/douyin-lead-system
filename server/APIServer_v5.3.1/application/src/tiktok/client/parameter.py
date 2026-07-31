#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：parameter.py
@IDE     ：PyCharm 

@Date    ：2025/4/22 11:24 
'''
import time
import urllib.parse

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "referer": "https://www.tiktok.com/"
}

async def app_headers(signature, host='api16-normal-useast5.tiktokv.us'):
    headers = {
        'X-SS-REQ-TICKET': str(round(time.time() * 1000)),
        'X-Gorgon': signature.get('X-Gorgon'),
        'X-Khronos': signature.get('X-Khronos'),
        'sdk-version': '1',
        'Accept-Encoding': 'gzip',
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; 22021211RC Build/V417IR) NewsArticle/8.4.2 tt-ok/3.10.0.2",
        'Cookie': "",
        'Host': "api16-normal-useast5.tiktokv.us",
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    return headers


async def root_comment_url_path(aweme_id, cursor, device_data):
    params = (f"aweme_id={aweme_id}&cursor={cursor}&count=20&forward_page_type=1&channel_id=0&user_avatar_shrink"
              f"=96_96&ad_pricing_type=0&load_type=0&iid={device_data['install_id']}&device_id={device_data['device_id']}"
              f"&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=250602&version_name=25.6.2&devi"
              f"ce_platform=android&ab_version=25.6.2&ssmix=a&device_type=2201123C&device_brand=Xiaomi&language=zh-Han"
              f"s&os_api=32&os_version=12&openudid=0dbcc63fca000305&manifest_version_code=2022506020&resolution=1080*"
              f"1920&dpi=480&update_version_code=2022506020&_rticket=1735970142533&app_type=normal&sys_region=CN&mcc_m"
              f"nc=31001&timezone_name=Asia%2FShanghai&carrier_region_v2=460&app_language=en&carrier_region=US&ac2=wi"
              f"fi5g&uoo=1&op_region=US&timezone_offset=28800&build_number=25.6.2&host_abi=arm64-v8a&locale=en&region"
              f"=CN&ts=1735970138&cdid=52cb5c9d-2e00-49df-a458-81a09c5a9242&is_pad=0&is_landscape=0")

    return params


async def sub_comment_url_path(aweme_id, cursor, comment_id, device_data):
    params = (f"comment_id={comment_id}&cursor={cursor}&count=30&top_ids&item_id={aweme_id}&insert_ids&channel_id=0&user"
              f"_avatar_shrink=96_96&need_translation=false&trg_lang&iid={device_data['install_id']}&device_id={device_data['device_id']}&ac=wifi&channel=googlepla"
              f"y&aid=1233&app_name=musical_ly&version_code=250602&version_name=25.6.2&device_platform=android&ab_versi"
              f"on=25.6.2&ssmix=a&device_type=2201123C&device_brand=Xiaomi&language=zh-Hans&os_api=32&os_version=12&open"
              f"udid=0dbcc63fca000305&manifest_version_code=2022506020&resolution=1080*1920&dpi=480&update_version_code"
              f"=2022506020&_rticket=1735970451768&app_type=normal&sys_region=CN&mcc_mnc=31001&timezone_name=Asia%2FSha"
              f"nghai&carrier_region_v2=460&app_language=en&carrier_region=US&ac2=wifi5g&uoo=1&op_region=US&timezone_of"
              f"fset=28800&build_number=25.6.2&host_abi=arm64-v8a&locale=en&region=CN&ts=1735970448&cdid=52cb5c9d-2e00"
              f"-49df-a458-81a09c5a9242&is_pad=0&is_landscape=0")

    return params


async def user_post_path(sec_uid, post_type, count, cursor, gen):
    params = (f"WebIdLastTime={int(time.time())}&aid=1988&app_language=zh-Hans&app_name=tiktok_web&browser_language=zh"
              f"-CN&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20"
              f"NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131."
              f"0.0.0%20Safari%2F537.36%20Edg%2F131.0.0.0&channel=tiktok_web&cookie_enabled=true&count={count}&coverFo"
              f"rmat=2&cursor={cursor}&data_collection_enabled=false&device_id={gen['device_id']}&device_platform=web_"
              f"pc&focus_state=false&from_page=user&history_len=5&is_fullscreen=false&is_page_visible=true&language=zh"
              f"-Hans&needPinnedItemIds=true&os=windows&post_item_list_request_type={post_type}&priority_region=&refe"
              f"rer=&region=US&screen_height=1080&screen_width=1920&secUid={sec_uid}&tz_name=Asia%2FShanghai&user_is"
              f"_login=false&webcast_language=zh-Hans")
    return params


async def general_search_path(keyword, cursor, search_id, gen):
    query = (f"WebIdLastTime={str(int(time.time()))}&aid=1988&app_language=zh-Hans&app_name=tiktok_web&browser_language"
             f"=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Maci"
             f"ntosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20C"
             f"rome%2F134.0.0.0%20Safari%2F537.36%20Edg%2F134.0.0.0&channel=tiktok_web&cookie_enabled=true&data_collec"
             f"tion_enabled=true&device_id={gen['device_id']}&device_platform=web_pc&device_type=web_h265&focus_state=t"
             f"rue&from_page=search&history_len=4&is_fullscreen=false&is_page_visible=true&"
             f"keyword={urllib.parse.quote(keyword)}&odinId={gen['odinId']}&offset={cursor}&os=mac&priority_region=&"
             f"referer=&region=FR&screen_height=1112&screen_width=1710&search_id={search_id}&search_source=normal_sea"
             f"rch&tz_name=Asia%2FShanghai&user_is_login=false&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_"
             f"x%22%3A%7B%22search_engine%22%3A%7B%22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_gene"
             f"ral_user_live_card%22%3A1%7D%7D%2C%22search_server%22%3A%7B%7D%7D%7D&webcast_language=zh-Hans")

    return query


async def search_user_path(keyword, cursor, search_id, gen):
    query = (f"WebIdLastTime=0&aid=1988&app_language=zh-Hans&app_name=tiktok_web&browser_language=zh-CN&browser_"
             f"name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%20"
             f"10.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F13"
             f"6.0.0.0%20Safari%2F537.36%20Edg%2F136.0.0.0&channel=tiktok_web&cookie_enabled=true&cursor={cursor}&da"
             f"ta_collection_enabled=false&device_id={gen['device_id']}&device_platform=web_pc&focus_state=false&f"
             f"rom_page=search&history_len=7&is_fullscreen=false&is_page_visible=true&k"
             f"eyword={urllib.parse.quote(keyword)}&odinId={gen['odinId']}&os=windows&priority_region=&referer=&r"
             f"egion=US&screen_height=1440&screen_width=2560&search_id={search_id}&tz_name=Asia%2FShanghai&use"
             f"r_is_login=false&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%"
             f"22%3A%7B%22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_general_user_live_card%22%"
             f"3A1%7D%7D%2C%22search_server%22%3A%7B%7D%7D%7D&webcast_language=zh-Hans")
    return query


async def search_item_path(keyword, cursor, search_id, gen):
    query = (f"WebIdLastTime={str(int(time.time()))}&aid=1988&app_language=zh-Hans&app_name=tiktok_web&browser_language"
             f"=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Maci"
             f"ntosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20"
             f"Chrome%2F134.0.0.0%20Safari%2F537.36%20Edg%2F134.0.0.0&channel=tiktok_web&cookie_enabled=true&count=20"
             f"&data_collection_enabled=true&device_id={gen['device_id']}&device_platform=web_pc&focus_state=true&fr"
             f"om_page=search&history_len=11&is_fullscreen=false&is_page_visible=true&k"
             f"eyword={urllib.parse.quote(keyword)}&odinId={gen['odinId']}&offset={cursor}&os=mac&priority_region=&refe"
             f"rer=&region=FR&screen_height=1112&screen_width=1710&search_id={search_id}&tz_name=Asia%2FShanghai&user_i"
             f"s_login=false&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%22%3A%7B%"
             f"22ies_mt_user_live_video_card_use_libra%22%3A1%2C%22mt_search_general_user_live_card%22%3A1%7D%7D%2C%22"
             f"search_server%22%3A%7B%7D%7D%7D&webcast_language=zh-Hans")

    return query

