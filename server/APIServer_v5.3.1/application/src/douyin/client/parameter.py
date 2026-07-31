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
@File    ：parameter.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/12 11:09 
@WebSite ：
'''
import json
import urllib.parse
import time
import uuid
from typing import Union

PC_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
X_PC_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
PC_HEADERS = {
    "User-Agent": PC_UA,
    "Referer": "https://www.douyin.com/",
    "Accept-Language": 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

APP_HEADERS = {
    'sdk-version': '1',
    'Accept-Encoding': 'gzip',
    'User-Agent': "ttnet okhttp/3.10.0.2",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'Keep-Alive',
    'X-SS-REQ-TICKET': str(int(time.time() * 1000)),
}
MOBILE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/125.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Referer": "https://www.douyin.com/",
    "Host": "m.douyin.com",
}

IME_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) douyinim/1.1.21 Chrome/108.0.5359.215 Electron/22.3.18-tt.8.release.main.39 TTElectron/22.3.18-tt.8.release.main.39 Safari/537.36",
    "referer": "https://imdesktop.douyin.com",
}

ITEM_ID_PATTERNS = {
    "/video/": r'/video/([^/?]+)',
    "/slides/": r'/slides/([^/?]+)',
    "/note/": r'/note/([^/?]+)',
    "/hashtag/": r'/hashtag/([^/?]+)',
    "/music/": r'/music/([^/?]+)',
    "/playlet/": r'playlet/detail/([^/?]+)',
    "/challenge/": r'/challenge/([^/?]+)',
    "douyin/webcast": r'/douyin/webcast/reflow/([^/?]+)',
    "/live.douyin.com/": r'live.douyin.com/([^/?]+)',
    "/user/": r'(?:sec_uid=([^&]+)|/user/([^/?]+))',
}

ANY_ACCOUNT_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': PC_UA,
    'Host': 'www.douyin.com',
    'Connection': 'keep-alive'
}


async def params_v2_path():
    params_v2 = f"os_version=16.1.1&app_name=douyin_lite&ac=wifi&appTheme=light&js_sdk_version=3.55.0.5&version_code=32.9.0&channel=App%20Store&tma_jssdk_version=3.55.0.5&os_api=18&need_personal_recommend=1&device_platform=ipad&device_type=iPad13,19&is_guest_mode=0&build_number=329009&minor_status=0&aid=2329&mcc_mnc=&screen_width=1640&package=com.ss.iphone.ugc.aweme.lite&cdid={str(uuid.uuid4())}&app_version=32.9.0&device_score=10.6402&from_group_id=7532807169739279659&source=live_search&address_book_access=2"
    return params_v2


async def aweme_detail_path(aweme_id, device_data):
    path = (f"/aweme/v1/aweme/detail/?aweme_id={aweme_id}&iid={device_data['install_id_str']}&"
            f"device_id={device_data['device_id_str']}&_rticket={round(time.time() * 1000)}&"
            f"first_launch_timestamp={int(time.time())}&ts={int(time.time())}&start_time=0&has_total=true&total=&"
            f"danmaku_density=-1&authentication_token=&duration=&is_lvideo=false&&ac=wifi&channel=douyinweb1_64"
            f"&app_name=aweme&version_code=270800&version_name=27.8.0&device_platform=android&os=android&ssmix=a&"
            f"device_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&aid=1128&"
            f"manifest_version_code=270801&resolution=1080*1920&dpi=480&update_version_code=27809900&"
            f"package=com.ss.android.ugc.aweme&mcc_mnc=46000&last_deeplink_update_version_code=0&"
            f"cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&"
            f"appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&cdid=")
    return path


async def mulptile_aweme_detail_path(device_data):
    path = (f"/aweme/v1/multi/aweme/detail/?location_permission=1&iid={device_data['install_id_str']}&device_id="
            f"{device_data['device_id_str']}&ac=wifi&channel=doutui_1128_android_101824&aid=1128&app_name=aweme&"
            f"version_code=270900&version_name=27.9.0&device_platform=android&os=android&ssmix=a&device_type=SM-G9910"
            f"&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270901&resolution="
            f"1080*1920&dpi=480&update_version_code=27909900&_rticket={round(time.time() * 1000)}&first_launch_timestamp={int(time.time())}&"
            f"last_deeplink_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal"
            f"&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&ts={int(time.time())}&"
            f"cdid=22f8e095-3268-4124-83a1-c48311f498c7")
    return path


async def aweme_detail_v4_path(aweme_id):
    path = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&update_version_code=170400&pc_"
            f"client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=0&cpu_core_num=12&version_code=190500&ve"
            f"rsion_name=19.5.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser"
            f"_platform=Win32&browser_name=Edge&browser_version=141.0.0.0&browser_online=true&engine_name=Blink&engine"
            f"_version=141.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type="
            f"4g&round_trip_time=50&webid=&uifid=&msToken=")

    return path


async def user_data_path(sec_user_id):
    path = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&"
            f"update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true"
            f"&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox"
            f"&browser_version=124.0&browser_online=true&engine_name=Gecko&engine_version=122.0.0.0&os_name=Windows"
            f"&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&msToken=&sec_user_id={sec_user_id}")

    return path


async def user_data_v2_path(sec_user_id, device_data):
    path = (f"/aweme/v1/user/?sec_user_id={sec_user_id}&address_book_access=2&manifest_version_code=912"
            f"&_rticket={str(int(time.time() * 1000))}&app_type=normal&iid={device_data['install_id_str']}"
            f"&channel=wandoujia_0303&device_type=SM-G9910&language=zh&resolution=1080*1920&update_version_code=9127"
            f"&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id_str']}&mcc_mnc=46000&os_version=12"
            f"&version_code=912&app_name=douyin_lite&version_name=27.8.0&device_brand=samsung&ssmix=a"
            f"&device_platform=android&aid=2329&ts={str(int(time.time()))}")

    return path


async def user_data_v5_path(sec_user_id, device_data):
    path = (f"/webcast/user/?packed_level=2&sec_target_uid={sec_user_id}"
            f"&webcast_sdk_version=3200&webcast_language=zh&webcast_locale=zh_CN&webcast_gps_access=1&"
            f"current_network_quality_info={{}}&device_score=10.0&address_book_access=1&"
            f"is_pad=false&is_android_pad=0&is_landscape=false&carrier_region=CN"
            f"&sec_user_id={sec_user_id}&iid={device_data['install_id']}&"
            f"device_id={device_data['device_id']}&ac=wifi&channel=doutui_1128_android_101824&"
            f"aid=1128&app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=android&"
            f"os=android&ssmix=a&device_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&"
            f"os_version=12&manifest_version_code=270901&resolution=1080*1920&dpi=480&update_version_code=27909900"
            f"&_rticket={round(time.time() * 1000)}&first_launch_timestamp={int(time.time())}&last_deeplink_update_version_code=0&"
            f"cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&"
            f"need_personal_recommend=1&is_android_fold=0&ts={int(time.time())}&cdid=22f8e095-3268-4124-83a1-c48311f498c7")
    return path


async def user_detail_by_u_id(user_id, device_data):
    path = (f"/aweme/v1/user/?user_id={user_id}&address_book_access=2&manifest_version_code=912"
            f"&_rticket={str(int(time.time() * 1000))}&app_type=normal&iid={device_data['install_id_str']}"
            f"&channel=wandoujia_0303&device_type=SM-G9910&language=zh&resolution=1080*1920&update_version_code=9127"
            f"&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id_str']}&mcc_mnc=46000&os_version=12"
            f"&version_code=912&app_name=douyin_lite&version_name=27.8.0&device_brand=samsung&ssmix=a"
            f"&device_platform=android&aid=2329&ts={str(int(time.time()))}")

    return path


async def user_post_path(sec_user_id, max_cursor, count, filter_type, device_data):
    path = (
        f"/aweme/v1/{'filter' if filter_type == '3' else 'aweme'}/post/?publish_video_strategy_type=2&source=0&user_avatar_shrink=144_144&"
        f"video_cover_shrink=372_495&filter_type={filter_type}&need_time_list=0&max_cursor={max_cursor}&sec_user_id="
        f"{sec_user_id}&count={count}&show_live_replay_s"
        f"trategy=1&is_order_flow=0&page_from=2&location_permission=1&collects_id&familiar_collects=0&page_scene=1"
        f"&post_serial_strategy=0&iid={device_data['install_id_str']}&device_id={device_data['device_id_str']}&ac=wifi&channel=doutui_1128_an"
        f"droid_101824&aid=1128&app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=android&os=a"
        f"ndroid&ssmix=a&device_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_ver"
        f"sion_code=270901&resolution=1080*1920&dpi=480&update_version_code=27909900&_rticket=1758086357789&first_la"
        f"unch_timestamp=1741070589&last_deeplink_update_version_code=27909900&cpu_support64=true&host_abi=arm64-v8a"
        f"&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0"
        f"&is_android_fold=0&ts=1758086357&cdid=22f8e095-3268-4124-83a1-c48311f498c7")
    return path


async def user_post_path_v2(sec_user_id, max_cursor, count, user_id, device_data):
    path = (
        f"/aweme/v1/aweme/post/?manifest_version_code=590&_rticket={round(time.time() * 1000)}&iid={device_data['install_id']}&cdid_ts=1739008367402&channel=tengxun5"
        f"&device_type=22021211RC&language=zh&host_abi=armeabi-v7a&resolution=&openudid="
        f"&update_version_code=99008&cdid={str(uuid.uuid4())}&os_api=32&dpi=480&ac=wifi&"
        f"device_id={device_data['device_id']}&os_version=12&version_code=990&tma_jssdk_version=2.10.1.5&app_name=video_article"
        f"&ab_version&version_name=9.9.0&device_brand=Redmi&ssmix=a&device_platform=android&aid=32&rom_version="
        f"V417IR+release-keys&req_source=xigua_applet&user_id={user_id}&filter_private=1&count={count}"
        f"&max_cursor={max_cursor}&sec_user_id={sec_user_id}")
    return path


async def user_post_by_uid_path(user_id, max_cursor, count, filter_type, device_data):
    path = (f'/aweme/v1/{"filter" if filter_type == "3" else "aweme"}/post/?source=0&user_avatar_shrink=96_96&'
            f'video_cover_shrink=248_330&publish_video_strategy_type=2&max_cursor={max_cursor}&user_id={user_id}'
            f'&count={count}&filter_type={filter_type}&show_live_replay_strategy=1&is_order_flow=0&os_api=32&'
            f'device_type=WLZ-AN00&ssmix=a&manifest_version_code=180401&dpi=280&app_name=aweme&version_name=29.8.0'
            f'&ts=1711525720&cpu_support64=false&app_type=normal&appTheme=dark&ac=wifi&host_abi=armeabi-v7a&'
            f'update_version_code=18409900&channel=gray_13700500&_rticket=1610866168530&device_platform=android&'
            f'iid={device_data["install_id_str"]}&version_code=180400&device_id={device_data["device_id_str"]}&'
            f'resolution=1920*1080&os_version=12&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46000&'
            f'package=com.ss.android.ugc.aweme')
    return path


async def user_data_v4_path(sec_user_id, did, iid, awemeim_guid):
    path = (f"https://imdesktop.douyin.com/aweme/v1/web/user/profile/other/?aid=339757&version_name=1.1.21&"
            f"version_code=1.1.21&device_platform=win32&sec_user_id={sec_user_id}&source=together&os_version=10.0.22631"
            f"&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&"
            f"browser_version=&browser_online=true&cookie_enabled=true&device_id={did}&did={did}&iid={iid}&"
            f"awemeim_guid={awemeim_guid}&channel=")
    return path


async def user_post_v2_path(sec_user_id, count, max_cursor):
    path = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id={sec_user_id}&max_cursor={max_cursor}&"
            f"locate_query=false&show_live_replay_strategy=1&need_time_list=1&time_list_query=0&whale_cut_token="
            f"&cut_version=1&count={count}&publish_video_strategy_type=2&from_user_page=1&update_version_code=170400"
            f"&pc_client_type=1&pc_libra_divert=Windows&version_code=290100&version_name=29.1.0&cookie_enabled=true&"
            f"screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&"
            f"browser_version=130.0.0.0&browser_online=true&engine_name=Blink&engine_version=130.0.0.0&os_name=Windows"
            f"&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&"
            f"round_trip_time=50&webid=&msToken=")
    return path


async def user_mix_path(sec_user_id, count, cursor, device_data):
    path = (f"/aweme/v1/mix/list/?sec_user_id={sec_user_id}&count={count}&cursor={cursor}&manifest_version_code=140900"
            f"&_rticket={round(time.time() * 1000)}&app_type=normal&iid={device_data['install_id_str']}&"
            f"channel=wandoujia_2329_0608&device_type=SM-G9910&language=zh&cpu_support64=true&host_abi=armeabi-v7a&uuid="
            f"&resolution=1080*1920&openudid=&update_version_code=14909900&cdid=&os_api=32&mac_address=&dpi=480&ac=wifi"
            f"&device_id={device_data['device_id_str']}&mcc_mnc=46000&tool_grey_user=0&os_version=12&version_code=140900"
            f"&app_name=douyin_lite&version_name=30.1.0&device_brand=samsung&ssmix=a&device_platform=android&aid=2329"
            f"&ts={int(time.time())}")
    return path


async def mix_info_path(mix_id, device_data):
    path = (f"/aweme/v1/mix/detail/?mix_id={mix_id}&manifest_version_code=912&_rticket={round(time.time() * 1000)}"
            f"&app_type=normal&iid={device_data['install_id_str']}&channel=wandoujia_0303&device_type=SM-G9910&"
            f"language=zh&uuid=&resolution=1080*1920&openudid=&update_version_code=9127&cdid=&os_api=32&dpi=480&"
            f"ac=wifi&device_id={device_data['device_id_str']}&mcc_mnc=46000&os_version=12&version_code=912&"
            f"app_name=douyin_lite&version_name=9.1.2&device_brand=samsung&ssmix=a&device_platform=android&aid=2329"
            f"&ts={int(time.time())}")
    return path


async def mix_aweme_list_path(mix_id, count, cursor, device_data):
    path = (f"/aweme/v1/mix/aweme/?mix_id={mix_id}&cursor={cursor}&count={count}&manifest_version_code=912&"
            f"_rticket={round(time.time() * 1000)}&app_type=normal&iid={device_data['install_id_str']}&"
            f"channel=wandoujia_0303&device_type=SM-G9910&language=zh&uuid=&resolution=1080*1920&openudid=&"
            f"update_version_code=9127&cdid=&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id_str']}"
            f"&mcc_mnc=46000&os_version=12&version_code=912&app_name=douyin_lite&version_name=9.1.2&"
            f"device_brand=samsung&ssmix=a&device_platform=android&aid=2329&ts={int(time.time())}")
    return path


async def search_user_aweme_path(user_uid, keyword, count, offset, search_id):
    params = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_personal_home_video&"
              f"search_source=normal_search&search_scene=douyin_search&sort_type=0&publish_time=0&is_filter_search=0"
              f"&query_correct_type=1&keyword={keyword}&enable_history=NaN"
              f"&offset={offset}&count={count}&from_user={user_uid}&pc_client_type=1&pc_libra_divert=Windows&support_h265=1"
              f"&support_dash=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&"
              f"screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version="
              f"135.0.0.0&browser_online=true&engine_name=Blink&engine_version=135.0.0.0&os_name=Windows&os_version"
              f"=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=&msToken=")
    if search_id:
        params += f"&search_id={search_id}"
    return params


async def user_fav_path(sec_user_id, count, max_cursor, device_data):
    path = (f'/aweme/v1/aweme/favorite/?invalid_item_count=0&is_hiding_invalid_item=0&max_cursor={max_cursor}'
            f'&sec_user_id={sec_user_id}&count={count}&manifest_version_code=110001&'
            f'_rticket={round(time.time() * 1000)}&app_type=normal&iid={device_data["install_id_str"]}&'
            f'channel=tengxun_new&device_type=SM-G9910&language=zh&cpu_support64=true&host_abi=armeabi-v7a&'
            f'uuid=&resolution=1080*1920&openudid=&update_version_code=11009900&cdid=&os_api=32&dpi=480&ac=wifi'
            f'&device_id={device_data["device_id_str"]}&mcc_mnc=46000&os_version=12&version_code=110000&app_name=aweme'
            f'&version_name=18.4.0&device_brand=samsung&ssmix=a&device_platform=android&aid=1128&ts={int(time.time())}')
    return path


async def aweme_root_comment_path(aweme_id, cursor, count, device_data):
    path = (
        f'/aweme/v2/comment/list/?aweme_id={aweme_id}&cursor={cursor}&count={count}&insert_ids&address_book_access=2'
        f'&gps_access=2&forward_page_type=1&channel_id=0&hotsoon_filtered_count=0&hotsoon_has_more=0&'
        f'follower_count=0&is_familiar=0&page_source=0&user_avatar_shrink=96_96&item_type=0&comment_aggregation=0'
        f'&top_query_word&is_guest_mode=0&manifest_version_code=180401&app_type=normal&'
        f'iid={device_data["install_id_str"]}&is_android_pad=0&channel=wandoujia_lesi_1128_1108&'
        f'device_type=SM-G9910&language=zh&cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*1920&'
        f'update_version_code=18409900&minor_status=0&appTheme=light&os_api=32&dpi=480&ac=wifi&'
        f'package=com.ss.android.ugc.aweme&device_id={device_data["device_id_str"]}&os=android&'
        f'mcc_mnc=46000&os_version=12&version_code=180400&app_name=aweme&version_name=26.9.0&device_brand=samsung'
        f'&need_personal_recommend=1&ssmix=a&device_platform=android&aid=1128&ts={int(time.time())}')
    return path


async def aweme_sub_comment_path(aweme_id, comment_id, cursor, count, device_data):
    path = (f'/aweme/v1/comment/list/reply/?comment_id={comment_id}&cursor={cursor}&count={count}&top_ids&'
            f'item_id={aweme_id}&insert_ids&channel_id=0&follower_count=0&is_familiar=0&user_avatar_shrink=96_96'
            f'&item_type=0&top_query_word&is_guest_mode=0&manifest_version_code=180401&_rticket={round(time.time() * 1000)}'
            f'&app_type=normal&iid={device_data["install_id_str"]}&is_android_pad=0&'
            f'channel=wandoujia_lesi_1128_1108&device_type=SM-G9910&language=zh&cpu_support64=true&'
            f'host_abi=armeabi-v7a&resolution=1080*1920&update_version_code=18409900&minor_status=0&appTheme=light&'
            f'os_api=32&dpi=480&ac=wifi&package=com.ss.android.ugc.aweme&'
            f'device_id={device_data["device_id_str"]}&os=android&os_version=12&version_code=180400&'
            f'app_name=aweme&version_name=21.4.0&device_brand=samsung&need_personal_recommend=1&ssmix=a&'
            f'device_platform=android&aid=1128&ts={int(time.time())}')

    return path


async def user_series_list_path(sec_user_id, cursor, count, device_data):
    path = (f'/aweme/v1/series/list/?cursor={cursor}&count=20&has_series_tab=0&sec_user_id={sec_user_id}&'
            f'manifest_version_code=110001&_rticket={str(round(time.time() * 1000))}&app_type=normal'
            f'&iid={device_data["install_id_str"]}&channel=tengxun_new&device_type=SM-G9910&language=zh'
            f'&cpu_support64=true&host_abi=armeabi-v7a&uuid=&resolution=1080*1920&openudid=&'
            f'update_version_code=11009900&cdid=&os_api=32&dpi=480&ac=wifi&device_id={device_data["device_id_str"]}'
            f'&mcc_mnc=46000&os_version=12&version_code=110000&app_name=aweme&version_name=30.2.0&device_brand=samsung'
            f'&ssmix=a&device_platform=android&aid=1128&ts={str(int(time.time()))}')

    return path


async def series_info_path(series_id, device_data):
    path = (f'/aweme/v1/series/detail/?&series_id={series_id}&_rticket={round(time.time() * 1000)}&app_type=normal&'
            f'iid={device_data["install_id_str"]}&channel=wandoujia_0303&device_type=SM-G9910&language=zh&uuid=&'
            f'resolution=2160*3840&openudid=f8bb31ec9541fb1b&update_version_code=9202&cdid=&os_api=32&dpi=960&ac=wifi&'
            f'device_id={device_data["device_id_str"]}&mcc_mnc=46000&os_version=12&version_code=920&app_name=douyin_lite'
            f'&version_name=30.2.0&device_brand=samsung&ssmix=a&device_platform=android&aid=2329&ts={int(time.time())}')
    return path


async def series_aweme_list_path(series_id, count, cursor, device_data):
    path = (f'/aweme/v1/series/aweme/?cursor={cursor}&pull_type=2&count={count}&series_id={series_id}&'
            f'manifest_version_code=110001&_rticket={str(round(time.time() * 1000))}&app_type=normal&'
            f'iid={device_data["install_id_str"]}&channel=tengxun_new&device_type=SM-G9910&language=zh&'
            f'cpu_support64=true&host_abi=armeabi-v7a&uuid=&resolution=1080*1920&openudid=&'
            f'update_version_code=11009900&cdid=&os_api=32&dpi=480&ac=wifi&device_id={device_data["device_id_str"]}&'
            f'mcc_mnc=46000&os_version=12&version_code=110000&app_name=aweme&version_name=30.2.0&device_brand=samsung'
            f'&ssmix=a&device_platform=android&aid=1128&ts={str(int(time.time()))}')
    return path


async def search_params_path(keyword, count, cursor, search_id: Union[None, str], search_session_id: Union[None, str]):
    params = {
        "in_sp_time": "0",
        "search_id": search_id,
        "query_correct_type": "1",
        "keyword": keyword,
        "start_session": "0",
        "search_source": "switch_tab",
        "search_request_id": search_id,
        "count": count,
        "search_session_id": search_session_id,
        "cursor": cursor,
        "hot_search": "0",
        "search_rerank_info": "{\"poi_send_back\":{\"life_service_user_history_actions\":[],\"user_device_feature\":{\"volume\":0.75,\"dark_mode\":0,\"brightness\":0.30000001192092896,\"network_status\":\"WiFi\",\"headphones\":0,\"is_charging\":1,\"__dirty__\":[],\"is_low_power_mode\":0,\"is_mute\":0},\"user_status_prefer_feature\":{\"ohr\":\"3\",\"har\":\"3\"}}}",
        "is_mute_status": "0",
        "no_trace_search_switch": "off",
        "location_access": "0",
        "poi_search_info": "",
        "search_scene": "douyin_search",
        "enter_from": "homepage_hot",
    }
    return params


async def general_search_path(device_data, sort_type, publish_time, filter_duration, content_type, keyword, offset,
                              count, search_id=""):
    try:
        device_des = json.loads(device_data['description'])
    except:
        desc = device_data['description'].replace("'", '"')
        device_des = json.loads(desc)

    path = f'/aweme/v1/general/search/single/?ts={int(time.time())}&app_type=lite&manifest_version_code=9902002&_rticket={round(time.time() * 1000)}&iid={device_data["install_id_str"]}&channel=carplay_tmall_2955&device_type={device_des["device_type"]}&language=zh&uuid={device_des["device_id"]}&resolution={device_des["resolution"]}&openudid={device_des["openUDID"]}&update_version_code=9902002&cdid={device_des["cdid"]}&minor_status=0&os_api=28&dpi={device_des["density_dpi"]}&ac={device_des["access"]}&device_id={device_data["device_id_str"]}&is_autoplay=true&os_version=9&version_code=9902002&app_name=aweme&version_name=9.9.2002&device_brand=realme&ssmix=a&device_platform=android&aid=2955'
    data = {"keyword": keyword, "offset": offset, "count": count, "is_pull_refresh": "0",
            "search_source": "hot_search_section_search", "hot_search": "1", "latitude": "39.633542",
            "longitude": "115.109334", "search_id": "", "query_correct_type": "1"}
    if not sort_type == "0" or not publish_time == "0" or not filter_duration == "" or not content_type == "0":
        data.update({
            "filter_selected": json.dumps(
                {"sort_type": sort_type, "publish_time": publish_time, "filter_duration": filter_duration,
                 "content_type": content_type}),
            "is_filter_search": "1"
        })

    if search_id:
        data.update({
            "search_id": search_id
        })
    return path, data


async def stream_search_path_app(keyword, count):
    path = (
        f"/aweme/v1/general/search/stream/?ac=wifi&channel=doutui_1128_android_101824&aid=1128&app_name=aweme&versio"
        f"n_code=270900&version_name=27.9.0&device_platform=android&os=android&ssmix=a&device_type=SM-G9910&device"
        f"_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270901&resolution=1080*1920&dpi"
        f"=480&update_version_code=27909900&_rticket=1751267660433&first_launch_timestamp=1741070589&last_deeplink"
        f"_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status"
        f"=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&ts=1751267659&cdid=")
    data = {
        "filter_selected": "{\"sort_type\":\"0\",\"publish_time\":\"0\",\"filter_duration\":\"\"}",
        "from_group_id": "",
        "enter_from": "homepage_hot",
        "backtrace": "",
        "prefetch_id": "",
        "is_accessibility": "0",
        "general_search_inner_rerank": "0",
        "query_correct_type": "1",
        "double_column_switch": "0",
        "video_cover_shrink": "",
        "user_disable_double_column": "false",
        "mode": "",
        "client_prefetch_type": "press",
        "dynamic_type": "0",
        "large_font_mode": "0",
        "is_coin": "0",
        "keyword": keyword,
        "is_adapt_elder": "0",
        "effect_sdk_version": "15.4.0",
        "offset": "0",
        "search_scene": "douyin_search",
        "count": count,
        "from_author_id": "",
        "single_filter_aladdin": "0",
        "need_filter_settings": "1",
        "enable_history": "1",
        "search_source": "default_search_keyword",
        "hot_search": "1",
        "disable_synthesis": "0",
        "goods_info_version": "1",
        "disable_general_performance_opt_from_client": "1",
        "is_inner_search": "0",
        "is_refresh_request": "1",
        "disable_server_forecast": "0",
        "nearby_extra_data": "{\"nearby_tab_name\":\"同城\",\"has_groupon_tab\":true}",
        "client_engine_extra": "",
        "anchor_item_id": "",
        "is_after_locate": "false",
        "is_pull_refresh": "0",
        "is_filter_search": "0",
        "ssr_api_version": "1.2",
        "general_search_layout_type": "2",
        "extra": "{\"search_log_extra\":\"{\\\"caption_level\\\":\\\"\\\"}\"}",
        "client_extra": "{\"charging\":1,\"qoe\":82,\"har_info\":{}}",
        "nice_search_type": "general",
        "client_height": "640",
        "multi_mod": "0",
        "goods_info_count": "10",
        "loadmore_rerank": "2",
        "user_avatar_shrink": "",
        "lynx_ssr_props": "{\"isPad\":0,\"screenWidth\":360,\"fontScale\":1}",
        "enter_from_second": "",
        "client_width": "360",
        "search_id": "",
        "disable_double_column": "0",
        "disable_hotspot_new_card": "0",
        "epidemic_card_type": "0",
        "is_double_column_left": "0",
        "token": "search",
        "no_trace_search_switch": "off",
        "address_book_access": "2",
        "location_access": "2",
        "search_rerank_info": "null",
        "location_permission": "0",
        "device_score": "10.0"
    }
    return path, data


async def stream_search_path(keyword):
    path = (f"aid=6383&browser_language=zh-CN&browser_name=Edge&browser_online=true&browser_platform=MacIntel&browser"
            f"_version=135.0.0.0&channel=channel_pc_web&cookie_enabled=true&count=10&cpu_core_num=6&device_memory=8&d"
            f"evice_platform=webapp&downlink=5.05&effective_type=4g&enable_history=1&engine_name=Blink&engine_version"
            f"=135.0.0.0&from_group_id=&is_filter_search=0&keyword={keyword}&list_type=single&need_filter_settings=1&"
            f"offset=0&os_name=Mac+OS&os_version=10.15.7&pc_client_type=1&pc_libra_divert=Mac&platform=PC&query_corre"
            f"ct_type=1&round_trip_time=200&screen_height=1440&screen_width=2560&search_channel=aweme_general&search_"
            f"source=normal_search&support_dash=1&support_h265=1&version_code=190600&version_name=19.6.0")
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/',
        'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uifid': 'undefined',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Host': 'www.douyin.com',
        'Connection': 'keep-alive'
    }
    return path, headers


async def general_search_v2_path(keyword, offset, sort_type, publish_time, filter_duration, content_type, search_range,
                                 search_id,
                                 count):
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
    params = {"device_platform": "webapp",
              "aid": "6383",
              "channel": "channel_pc_web",
              "search_channel": "aweme_general",
              "enable_history": "1",
              "keyword": keyword,
              "search_source": "tab_search",
              "query_correct_type": "1",
              "from_group_id": "",
              "offset": offset,
              "count": count,
              "need_filter_settings": "0" if not offset == "0" else "1",
              "list_type": "multi",
              "search_id": search_id,
              "update_version_code": "170400",
              "pc_client_type": "1",
              "pc_libra_divert": "Windows",
              "support_h265": "1",
              "support_dash": "1",
              "cpu_core_num": "12",
              "version_code": "190600",
              "version_name": "19.6.0",
              "cookie_enabled": "true",
              "screen_width": "2560",
              "screen_height": "1440",
              "browser_language": "zh-CN",
              "browser_platform": "Win32",
              "browser_name": "Edge",
              "browser_version": "142.0.0.0",
              "browser_online": "true",
              "engine_name": "Blink",
              "engine_version": "142.0.0.0",
              "os_name": "Windows",
              "os_version": "10",
              "device_memory": "8",
              "platform": "PC",
              "downlink": "10",
              "effective_type": "4g",
              "round_trip_time": "50",
              "webid": "",
              }

    if not sort_type == "0" or not publish_time == "0":
        params.update({
            "filter_selected": json.dumps({"sort_type": sort_type, "publish_time": publish_time}),
            "is_filter_search": "1"
        })

    if not content_type == "0" or not filter_duration == "":
        params.update({
            "filter_selected": json.dumps(
                {"sort_type": sort_type, "publish_time": publish_time, "content_type": content_type,
                 "filter_duration": filter_duration}),
            "is_filter_search": "1"
        })
    if not search_range == "0":
        params.update({
            "filter_selected": json.dumps(
                {"sort_type": sort_type, "publish_time": publish_time, "content_type": content_type,
                 "filter_duration": filter_duration, "search_range": search_range}),
            "is_filter_search": "1"
        })

    return url, params


async def general_search_v3_path(keyword, offset, sort_type, publish_time, filter_duration, content_type, search_range,
                                 search_id,
                                 count):
    url = "https://www.douyin.com/aweme/v1/web/general/search/single/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_general",
        "enable_history": "1",
        "filter_selected": f"{{\"sort_type\":\"{sort_type}\",\"publish_time\":\"{publish_time}\",\"filter_duration\":\"{filter_duration}\",\"content_type\":\"{content_type}\"}}",
        "keyword": keyword,
        "search_source": "tab_search",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "disable_rs": "1",
        "offset": str(offset),
        "count": str(count),
        "need_filter_settings": "0",
        "list_type": "",
        "search_id": str(search_id),
        "update_version_code": "507002",
        "pc_client_type": "3",
        "pc_libra_divert": "Mac",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "8",
        "version_code": "190600",
        "version_name": "19.6.0",
        "cookie_enabled": "true",
        "screen_width": "1710",
        "screen_height": "1112",
        "browser_language": "zh-CN",
        "browser_platform": "MacIntel",
        "browser_name": "Chrome",
        "browser_version": "108.0.5359.215",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "108.0.5359.215",
        "os_name": "Mac+OS",
        "os_version": "10.15.7",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "9",
        "effective_type": "4g",
        "round_trip_time": "0",
        'webid': "",
        "msToken": "",
        "uifid": ""
    }
    if not sort_type == "0" or not publish_time == "0" or not filter_duration == "" or not content_type == "0" or not search_range == "0":
        params.update({
            "is_filter_search": "1"
        })

    return url, params


async def search_aweme_v3_path(keyword, offset, sort_type, publish_time, filter_duration, search_range,
                               search_id,
                               count):
    url = "https://www.douyin.com/aweme/v1/web/search/item/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_video_web",
        "enable_history": "1",
        "sort_type": sort_type,
        "publish_time": publish_time,
        "keyword": keyword,
        "search_source": "tab_search",
        "query_correct_type": "1",
        "is_filter_search": "1",
        "from_group_id": "",
        "disable_rs": "1",
        "offset": offset,
        "count": count,
        "need_filter_settings": "1",
        "list_type": "",
        "update_version_code": "507002",
        "pc_client_type": "3",
        "pc_libra_divert": "Mac",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "8",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1710",
        "screen_height": "1112",
        "browser_language": "zh-CN",
        "browser_platform": "MacIntel",
        "browser_name": "Chrome",
        "browser_version": "108.0.5359.215",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "108.0.5359.215",
        "os_name": "Mac+OS",
        "os_version": "10.15.7",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "9.3",
        "effective_type": "4g",
        "round_trip_time": "0",
        "filter_duration": filter_duration,
        "search_id": str(search_id),
        "search_range": search_range,
    }
    if not sort_type == "0" or not publish_time == "0" or not filter_duration == "" or not search_range == "0":
        params.update({
            "is_filter_search": "1"
        })

    return url, params


async def search_aweme_path(keyword, count, offset, sort_type, publish_time, filter_duration, search_range, search_id):
    url = "https://www.douyin.com/aweme/v1/web/search/item/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_video_web",
        "enable_history": "1",
        "keyword": keyword,
        "search_source": "tab_search",
        "query_correct_type": "1",
        "from_group_id": "",
        "offset": offset,
        "count": count,
        "need_filter_settings": "0" if not offset == "0" else "1",
        "list_type": "single",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "12",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "2560",
        "screen_height": "1440",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "142.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "142.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "100",
        # "webid": "",
        "search_id": search_id
    }

    if not sort_type == "0" or not publish_time == "0":
        params.update({
            "sort_type": sort_type,
            "publish_time": publish_time,
            "is_filter_search": "1"
        })

    if not filter_duration == "":
        params.update({
            "sort_type": sort_type,
            "publish_time": publish_time,
            "filter_duration": filter_duration,
            "is_filter_search": "1"
        })
    if not search_range == "0":
        params.update({
            "search_range": search_range,
            "is_filter_search": "1"

        })

    return url, params


async def search_aweme_v2_path(keyword, count, offset, sort_type, publish_time, filter_duration, device_data,
                               search_id):
    try:
        device_des = json.loads(device_data['description'])
    except:
        desc = device_data['description'].replace("'", '"')
        device_des = json.loads(desc)
    path = f'/aweme/v1/search/item/?ts={int(time.time())}&app_type=lite&manifest_version_code=9902002&_rticket={round(time.time() * 1000)}&iid={device_data["install_id_str"]}&channel=carplay_tmall_2955&device_type={device_des["device_type"]}&language=zh&uuid={device_des["device_id"]}&resolution={device_des["resolution"]}&openudid={device_des["openUDID"]}&update_version_code=9902002&cdid={device_des["cdid"]}&minor_status=0&os_api=28&dpi={device_des["density_dpi"]}&ac={device_des["access"]}&device_id={device_data["device_id_str"]}&is_autoplay=true&os_version=9&version_code=9902002&app_name=aweme&version_name=9.9.2002&device_brand=realme&ssmix=a&device_platform=android&aid=2955'
    data = {"keyword": keyword, "offset": offset, "count": count, "is_pull_refresh": "0",
            "search_source": "hot_search_section_search", "hot_search": "1", "latitude": "39.633542",
            "longitude": "115.109334", "search_id": "", "query_correct_type": "1"}
    if not sort_type == "0" or not publish_time == "0" or not filter_duration == "":
        data.update({
            "filter_selected": json.dumps(
                {"sort_type": sort_type, "publish_time": publish_time, "filter_duration": filter_duration}),
            "is_filter_search": "1"
        })

    if search_id:
        data.update({
            "search_id": search_id
        })
    return path, data


async def search_user_path(device_data):
    path = (f'/aweme/v1/discover/search/?manifest_version_code=912&_rticket={str(int(time.time() * 1000))}&'
            f'app_type=normal&iid={device_data["install_id_str"]}&channel=wandoujia_0303&device_type=SM-G9910'
            f'&language=zh&resolution=1080*1920&update_version_code=9127&os_api=32&dpi=480&ac=wifi&'
            f'device_id={device_data["device_id_str"]}&mcc_mnc=46000&os_version=12&version_code=912&app_name=douyin_lite'
            f'&version_name=9.1.2&device_brand=samsung&ssmix=a&device_platform=android&aid=2329&ts={str(int(time.time()))}')

    return path


async def search_user_v2_path(keyword, offset, search_id, count, douyin_user_type, douyin_user_fans):
    url = "https://www.douyin.com/aweme/v1/web/discover/search/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_user_web",
        "keyword": keyword,
        "search_source": "tab_search",
        "query_correct_type": "1",
        "from_group_id": "",
        "offset": offset,
        "count": count,
        "need_filter_settings": "0" if not offset == "0" else "1",
        "list_type": "",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "12",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "2560",
        "screen_height": "1440",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "139.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "139.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "100",
        "webid": "",
        "search_id": search_id

    }
    if not douyin_user_fans == "" or not douyin_user_type == "":
        params.update({
            "search_filter_value": json.dumps(
                {"douyin_user_fans": [douyin_user_fans], "douyin_user_type": [douyin_user_type]}),
            "is_filter_search": "1"
        })
    return url, params


async def search_user_v3_path(keyword, count, offset, douyin_user_type, douyin_user_fans, device_data, search_id):
    try:
        device_des = json.loads(device_data['description'])
    except:
        desc = device_data['description'].replace("'", '"')
        device_des = json.loads(desc)
    path = f'/aweme/v1/discover/search/?ts={int(time.time())}&app_type=lite&manifest_version_code=9902002&_rticket={round(time.time() * 1000)}&iid={device_data["install_id_str"]}&channel=carplay_tmall_2955&device_type={device_des["device_type"]}&language=zh&uuid={device_des["device_id"]}&resolution={device_des["resolution"]}&openudid={device_des["openUDID"]}&update_version_code=9902002&cdid={device_des["cdid"]}&minor_status=0&os_api=28&dpi={device_des["density_dpi"]}&ac={device_des["access"]}&device_id={device_data["device_id_str"]}&is_autoplay=true&os_version=9&version_code=9902002&app_name=aweme&version_name=9.9.2002&device_brand=realme&ssmix=a&device_platform=android&aid=2955'
    data = {"keyword": keyword, "cursor": offset, "count": count, "is_pull_refresh": "0",
            "search_source": "hot_search_section_search", "hot_search": "1", "latitude": "39.633542",
            "longitude": "115.109334", "search_id": "", "query_correct_type": "1", "nice_search_type": "user",
            "type": "1", }
    if not douyin_user_fans == "0" or not douyin_user_type == "0":
        data.update({
            "search_filter_value": json.dumps(
                {"douyin_user_fans": [douyin_user_fans], "douyin_user_type": [douyin_user_type]}),
            "is_filter_search": "1",
        })

    if search_id:
        data.update({
            "search_id": search_id
        })
    return path, data


async def search_music_path(keyword, count, cursor, device_data, search_id):
    try:
        device_des = json.loads(device_data['description'])
    except:
        desc = device_data['description'].replace("'", '"')
        device_des = json.loads(desc)
    path = f'/aweme/v1/music/search/?ts={int(time.time())}&app_type=lite&manifest_version_code=9902002&_rticket={round(time.time() * 1000)}&iid={device_data["install_id_str"]}&channel=carplay_tmall_2955&device_type={device_des["device_type"]}&language=zh&uuid={device_des["device_id"]}&resolution={device_des["resolution"]}&openudid={device_des["openUDID"]}&update_version_code=9902002&cdid={device_des["cdid"]}&minor_status=0&os_api=28&dpi={device_des["density_dpi"]}&ac={device_des["access"]}&device_id={device_data["device_id_str"]}&is_autoplay=true&os_version=9&version_code=9902002&app_name=aweme&version_name=9.9.2002&device_brand=realme&ssmix=a&device_platform=android&aid=2955'
    data = {"keyword": keyword,
            "cursor": cursor,
            "count": count, "is_pull_refresh": "0", "search_source": "hot_search_section_search", "hot_search": "1",
            "latitude": "39.633542", "longitude": "115.109334",
            "search_id": search_id,
            "query_correct_type": "1"}

    return path, data


async def music_path(music_id, device_data):
    path = (f"/aweme/v1/music/detail/?music_id={music_id}&click_reason=0&scene=1&is_guest_mode=0&"
            f"manifest_version_code=180401&_rticket={str(round(time.time() * 1000))}&app_type=normal&"
            f"iid={device_data['install_id_str']}&is_android_pad=0&channel=wandoujia_lesi_1128_1108&"
            f"device_type=SM-G9910&language=zh&cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*1920&"
            f"update_version_code=18409900&cdid=&minor_status=0&appTheme=light&os_api=32&dpi=480&ac=wifi&"
            f"package=com.ss.android.ugc.aweme&device_id={device_data['device_id_str']}&os=android&mcc_mnc=46000&"
            f"os_version=12&version_code=180400&app_name=aweme&version_name=30.2.0&device_brand=samsung&"
            f"need_personal_recommend=1&ssmix=a&device_platform=android&aid=1128&ts={str(int(time.time()))}")

    return path


async def music_aweme_path(music_id, cursor, count, device_data):
    path = (f"/aweme/v1/music/aweme/?music_id={music_id}&cursor={cursor}&count={count}&type=0&manifest_version_code=912"
            f"&_rticket={round(time.time() * 1000)}&app_type=normal&iid={device_data['install_id_str']}&"
            f"channel=wandoujia_0303&device_type=SM-G9910&language=zh&uuid=&resolution=1080*1920&openudid=&"
            f"update_version_code=9127&cdid=&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id_str']}&"
            f"mcc_mnc=46000&os_version=12&version_code=912&app_name=douyin_lite&version_name=30.2.0&"
            f"device_brand=samsung&ssmix=a&device_platform=android&aid=2329&ts={int(time.time())}")

    return path


async def search_live_path(keyword, offset, count, search_id):
    url = "https://www.douyin.com/aweme/v1/web/live/search/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_live",
        "keyword": keyword,
        "search_source": "switch_tab",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "disable_rs": "0",
        "offset": offset,
        "count": count,
        "need_filter_settings": "0",
        "list_type": "single",
        "pc_search_top_1_params": "{\"enable_ai_search_top_1\":1}",
        "search_id": search_id,
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "support_h265": "1",
        "support_dash": "1",
        "cpu_core_num": "12",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "2560",
        "screen_height": "1440",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "142.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "142.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": "",
        "msToken":""

    }
    return url, params


async def live_room_path(web_rid):
    url = (
        f"/webcast/room/web/enter/?aid=6383&app_name=douyin_web&live_id=1&device_platform=web&language=zh-CN&enter_from=web_share_link&"
        f"cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32"
        f"&browser_name=Edge&browser_version=130.0.0.0&web_rid={web_rid}")
    return url


async def live_user_path(room_id, sort_type):
    params = (f"aid=6383&app_name=douyin_web&live_id=1&device_platform=web&language=zh-CN&enter_from=page_refresh&"
              f"cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform="
              f"Win32&browser_name=Edge&browser_version=124.0.0.0&webcast_sdk_version=2450&room_id={room_id}&rank_type=30")

    return params


async def search_hash_tag_path(keyword, cursor, count, search_id):
    params = (f"keyword={urllib.parse.quote(keyword)}&channel=channel_pc_web&cursor={cursor}&count={count}&"
              f"device_platform=webapp&aid=6383&pc_client_type=1&search_id={search_id}&webid=&msToken=")
    return params


async def search_challenge_path(keyword, count, cursor, search_id, device_data):
    path = (
        f'/aweme/v2/challenge/search/?manifest_version_code=912&_rticket={str(round(time.time() * 1000))}&app_type=normal'
        f'&iid={device_data["install_id_str"]}&channel=wandoujia_0303&device_type=SM-G9910&language=zh&'
        f'uuid=866084040106293&resolution=1080*1920&openudid=be2ed3deb0633656&update_version_code=9127&'
        f'cdid=d916ab59-80f4-4cc8-b0be-cbf7a4c1fa77&os_api=32&dpi=480&ac=wifi&'
        f'device_id={device_data["device_id_str"]}&mcc_mnc=46000&os_version=12&version_code=912&'
        f'app_name=douyin_lite&version_name=16.1.0&device_brand=samsung&ssmix=a&device_platform=android&'
        f'aid=2329&ts={str(int(time.time()))}')

    data = {"cursor": cursor, "keyword": keyword, "count": count, "is_pull_refresh": "1", "hot_search": "0",
            "search_id": search_id, "query_correct_type": "1"}

    return path, data


async def search_challenge_path_v2(keyword, cursor, count, device_data, search_id):
    try:
        device_des = json.loads(device_data['description'])
    except:
        desc = device_data['description'].replace("'", '"')
        device_des = json.loads(desc)
    path = f'/aweme/v2/search/challenge/?ts={int(time.time())}&app_type=lite&manifest_version_code=9902002&_rticket={round(time.time() * 1000)}&iid={device_data["install_id_str"]}&channel=carplay_tmall_2955&device_type={device_des["device_type"]}&language=zh&uuid={device_des["device_id"]}&resolution={device_des["resolution"]}&openudid={device_des["openUDID"]}&update_version_code=9902002&cdid={device_des["cdid"]}&minor_status=0&os_api=28&dpi={device_des["density_dpi"]}&ac={device_des["access"]}&device_id={device_data["device_id_str"]}&is_autoplay=true&os_version=9&version_code=9902002&app_name=aweme&version_name=9.9.2002&device_brand=realme&ssmix=a&device_platform=android&aid=2955'
    data = {"keyword": keyword,
            "cursor": cursor,
            "count": count, "is_pull_refresh": "0", "search_source": "hot_search_section_search", "hot_search": "0",
            "latitude": "39.633542", "longitude": "115.109334",
            "search_id": search_id,
            "query_correct_type": "1"}

    return path, data


async def hash_tag_info_path(keyword, device_data):
    path = (f'/aweme/v1/commerce/challenge/detail/?click_reason=0&query_type=1&rec_age_stage=0&'
            f'hashtag_name={keyword}&is_guest_mode=0&manifest_version_code=180401&'
            f'_rticket={int(round(time.time() * 1000))}&app_type=normal&iid={device_data["install_id"]}&'
            f'is_android_pad=0&channel=wandoujia_lesi_1128_1108&device_type=SM-G9910&language=zh&'
            f'cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*1920&update_version_code=18409900'
            f'&cdid=&minor_status=0&appTheme=light&os_api=32&dpi=480&ac=wifi&package=com.ss.android.ugc.aweme&'
            f'device_id={device_data["device_id"]}&os=android&mcc_mnc=46000&os_version=12&version_code=180400&'
            f'app_name=aweme&version_name=18.4.0&device_brand=samsung&need_personal_recommend=1&ssmix=a&'
            f'device_platform=android&aid=1128&ts={int(time.time())}')
    return path


async def hash_tag_aweme_path(ch_id, cursor, sort_type, count, device_data):
    path = (f"/aweme/v1/challenge/aweme/?cursor={cursor}&enter_from=search_result&count={count}&query_type=0&"
            f"source=challenge_video&type=5&is_order_flow=0&video_cover_shrink=372_496&show_type=0&"
            f"sort_type={sort_type}&ch_id={ch_id}&location_permission=1&_rticket={round(time.time() * 1000)}&"
            f"first_launch_timestamp={int(time.time())}&last_deeplink_update_version_code=0&need_personal_recommend=1"
            f"&is_android_fold=0&ts={int(time.time())}&ac=wifi&aid=1128&appTheme=light&app_name=aweme&app_type=normal"
            f"&cdid=&channel=douyinweb1_64&cpu_support64=true&device_brand=samsung&device_id={device_data['device_id']}"
            f"&device_platform=android&device_type=SM-G9910&dpi=480&host_abi=arm64-v8a&iid={device_data['install_id']}&"
            f"is_android_pad=0&is_guest_mode=0&language=zh&manifest_version_code=270801&minor_status=0&os=android&"
            f"os_api=32&os_version=12&resolution=1080*1920&ssmix=a&update_version_code=27809900&version_code=270800&"
            f"version_name=27.8.0")

    return path


async def hash_tag_aweme_path_v2(keyword, cursor, sort_type, count, device_data):
    path = (f"/aweme/v1/challenge/aweme/?cursor={cursor}&from_group_id=7470353668047506745&enter_from=homepage_hot&"
            f"latitude=23.1806944025&count={count}&query_type=1&source=challenge_video&type=5&is_order_flow=0&"
            f"hashtag_name={urllib.parse.quote(keyword)}&sort_type={sort_type}&mac_address=&"
            f"longitude=113.4126737725&manifest_version_code=140901&_rticket=1739354306264&app_type=normal&"
            f"iid={device_data['install_id']}&channel=tengxun_1128_0226&device_type=SM-G9910&language=zh&"
            f"cpu_support64=true&host_abi=armeabi-v7a&uuid=863765046433912&resolution=1080*1920&"
            f"openudid=27bdca0d81e36f2e&update_version_code=14909900&cdid=25ace9c9-c2e1-4f80-bab8-d9a528d6189a&"
            f"appTheme=dark&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id']}&os_version=12&"
            f"version_code=140900&app_name=aweme&version_name=27.9.0&device_brand=samsung&ssmix=a&"
            f"device_platform=android&aid=1128&ts=1739354305")

    return path


async def aweme_danmaku_path(aweme_id, start_time, end_time):
    path = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&app_name=aweme&"
            f"format=json&group_id={aweme_id}&item_id={aweme_id}&start_time={start_time}&end_time={end_time}&pc_client_type=1&"
            f"version_code=170400&version_name=17.4.0")
    return path


async def short_link_path(device_data, aweme_id="", sec_user_id="", is_video=True):
    if is_video:
        data = {
            "targets": f"https://www.iesdouyin.com/share/video/{aweme_id}/?region=CN&mid=&u_code=&did=&iid=&with_sec_d"
                       f"id=1&video_share_track_ver=&titleType=title&share_sign=&share_version=2709"
                       f"00&ts={int(time.time())}&from_aid=1128&from_ssr=1&utm_source=copy&utm_campaign=client_sha"
                       f"re&utm_medium=android&app=aweme",
            "belong": "aweme",
            "persist": "1"
        }
    else:
        data = {
            "targets": f"https://www.iesdouyin.com/share/user/{sec_user_id}?u_code=&did=&iid=&with_sec_did="
                       f"1&sec_uid=&from_ssr=1&from_aid=1128&timestamp={int(time.time())}&utm_source=copy&utm_campa"
                       f"ign=client_share&utm_medium=android&app=aweme",
            "belong": "aweme",
            "persist": "1"
        }
    path = (f"/shorten/?iid={device_data['install_id']}&device_id={device_data['device_id']}&ac=wifi&channel=doutui_11"
            f"28_android_101824&aid=1128&app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=and"
            f"roid&os=android&ssmix=a&device_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12"
            f"&manifest_version_code=270901&resolution=1080*1920&dpi=480&update_version_code=27909900&_rtick"
            f"et={round(time.time() * 1000)}&first_launch_timestamp=&last_deeplink_update_version_code=0&cpu_suppor"
            f"t64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_person"
            f"al_recommend=1&is_android_pad=0&is_android_fold=0&ts={int(time.time())}&cdid=")
    return path, data


async def aweme_qr_code_path(device_data, aweme_id):
    path = (f'/aweme/v1/fancy/qrcode/info/?is_guest_mode=0&manifest_version_code=180401&_rticket=1715581537439&'
            f'app_type=normal&iid={device_data["install_id_str"]}&is_android_pad=0&channel=wandoujia_lesi_1128_1108&'
            f'device_type=SM-G9910&language=zh&cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*1920&'
            f'update_version_code=18409900&cdid=e4c1c27d-b612-4ee4-a104-e8ece2dcbb7a&minor_status=0&appTheme=light&'
            f'os_api=32&dpi=480&ac=wifi&package=com.ss.android.ugc.aweme&device_id={device_data["device_id"]}&'
            f'os=android&mcc_mnc=46000&os_version=12&version_code=180400&app_name=aweme&version_name=18.4.0&'
            f'device_brand=samsung&need_personal_recommend=1&ssmix=a&device_platform=android&aid=1128&ts=1715581536')
    data = {"schema_type": "1", "object_id": aweme_id, "qrcode_type": "0"}
    return path, data


async def search_sug_path(keyword, device_data):
    path = (f'/aweme/v1/search/sug/?keyword={keyword}&source=general&from_group_id=&no_trace_search_switch=off&'
            f'enter_from=homepage_hot&sug_enter_type=3&sug_gap_time=7752&sug_coin=0&'
            f'_rticket={str(round(time.time() * 1000))}&first_launch_timestamp={int(time.time())}&'
            f'last_deeplink_update_version_code=0&need_personal_recommend=1&is_android_fold=0&ts={int(time.time())}&'
            f'ac=wifi&aid=1128&appTheme=light&app_name=aweme&app_type=normal&cdid=&channel=douyinweb1_64&'
            f'cpu_support64=true&device_brand=samsung&device_id={device_data["device_id_str"]}&device_platform=android'
            f'&device_type=SM-G9910&dpi=480&host_abi=arm64-v8a&iid={device_data["install_id_str"]}&is_android_pad=0&'
            f'is_guest_mode=0&language=zh&manifest_version_code=270801&minor_status=0&os=android&os_api=32&os_version=12'
            f'&resolution=1080*1920&ssmix=a&update_version_code=27809900&version_code=270800&version_name=27.8.0')
    return path


async def hot_spot_aladdin_path(sentence_id, sort_type, cursor, device_data):
    path = (f'/aweme/v1/hotspot/aladdin/item/list/?ala_src=douyin_hotspot_comment_list&'
            f'sentence_id={sentence_id}&insert_source=1&entrance=search_aladdin_card&cursor={cursor}&'
            f'sort_type={sort_type}&iid={device_data["install_id_str"]}&device_id={device_data["device_id_str"]}'
            f'&ac=wifi&channel=douyinweb1_64&aid=1128&app_name=aweme&version_code=270800&version_name=27.8.0&'
            f'device_platform=android&os=android&ssmix=a&device_type=SM-G9910&device_brand=samsung&language=zh&'
            f'os_api=32&os_version=12&manifest_version_code=270801&resolution=1080*1920&dpi=480&'
            f'update_version_code=27809900&_rticket={round(time.time() * 1000)}&first_launch_timestamp={int(time.time())}'
            f'&last_deeplink_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal'
            f'&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&'
            f'ts={int(time.time())}&cdid=')
    return path


async def user_profile_sale_path(sec_user_id, device_data):
    path = (f'/window/header/bff/?sec_author_id={sec_user_id}&pass_through_api=%7B%22entrance_location%22%3A%22others_'
            f'homepage%22%2C%22pre_store_source_page%22%3A%22homepage_hot%22%2C%22pre_store_group_type%22%3A%22vid'
            f'eo%22%2C%22pre_group_id%22%3A%227390749725718269219%22%2C%22pre_product_id%22%3A%22%22%2C%22pre_live_'
            f'id%22%3A%22%22%2C%22store_type%22%3A%22window%22%2C%22live_user_act_params%22%3A%22%22%2C%22ecom_scene_'
            f'id%22%3A%221004%22%7D&upgrade_version=1&scene_type=0&iid={device_data["install_id_str"]}&'
            f'device_id={device_data["device_id_str"]}&ac=wifi&channel=douyinweb1_64&aid=1128&app_name=aweme&'
            f'version_code=270800&version_name=27.8.0&device_platform=android&os=android&ssmix=a&device_type='
            f'SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270801&'
            f'resolution=1080*1920&dpi=480&update_version_code=27809900&_rticket={round(time.time() * 1000)}&'
            f'first_launch_timestamp={int(time.time())}&last_deeplink_update_version_code=0&cpu_support64=true&'
            f'host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_personal_recommend=1'
            f'&is_android_pad=0&is_android_fold=0&ts={int(time.time())}&cdid=e7c85b3c-98c3-4f94-8742-4bdfdc0971a2')
    return path


async def nearby_aweme_path(city_code, latitude, longitude, device_data, lock_device=False):
    min_cursor = "0"
    if lock_device:
        min_cursor = "-1"
    path = (
        f"/aweme/v1/nearby/feed/?max_cursor=0&min_cursor={min_cursor}&count=20&feed_style=1&filter_warn=0&city={city_code}"
        f"&latitude={latitude}&longitude={longitude}&poi_class_code=0&pull_type=1&location_permission=1&"
        f"manifest_version_code=912&_rticket={round(time.time() * 1000)}&app_type=normal&"
        f"iid={device_data['install_id_str']}&channel=wandoujia_0303&device_type=SM-G9910&language=zh&"
        f"uuid=866084040106293&resolution=1080*1920&openudid=be2ed3deb0633656&update_version_code=9127&"
        f"cdid=256a345b-fba1-482e-8bba-55e25975b1a9&os_api=32&dpi=480&ac=wifi&device_id={device_data['device_id']}&"
        f"mcc_mnc=46000&os_version=12&version_code=912&app_name=douyin_lite&version_name=9.1.2&device_brand=samsung&"
        f"ssmix=a&device_platform=android&aid=2329&ts={int(time.time())}")
    return path


async def share_to_scheme_path(url, device_data):
    path = (
        f"/aweme/v1/schema/trans/?url={urllib.parse.quote(url)}&support_type=16&iid={device_data['install_id']}&device_id="
        f"{device_data['device_id']}&ac=wifi&channel=oppo_8663_411&aid=8663&app_name=aweme_hotsoon&"
        f"version_code=220308&version_name=22.3.8&device_platform=android&os=android&ssmix=a&device_type="
        f"MI%2B5s&device_brand=Xiaomi&language=zh&os_api=32&os_version=12&manifest_version_code=220308&resolution"
        f"=1080*1920&dpi=480&update_version_code=22300805&_rticket=1741744519118&package=com.ss.android.ugc.live&"
        f"mcc_mnc=46000&cpu_support64=true&host_abi=armeabi-v7a&is_guest_mode=0&app_type=normal&minor_status=0&"
        f"appTheme=light&need_personal_recommend=1&is_android_pad=0&ts=1741744517&cdid=&md=0")
    return path


async def check_user_live_path(sec_user_id, device_data):
    path = (
        f"/webcast/distribution/check_user_live_status/?iid={device_data['install_id']}&device_id={device_data['device_id']}&ac="
        f"wifi&channel=oppo_8663_411&aid=8663&"
        f"app_name=aweme_hotsoon&version_code=220308&version_name=22.3.8&device_platform=android&os=android&"
        f"ssmix=a&device_type=MI+5s&device_brand=Xiaomi&language=zh&os_api=32&os_version=12&"
        f"manifest_version_code=220308&resolution=1080*1920&dpi=480&update_version_code=22300805&"
        f"_rticket={round(time.time() * 1000)}&package=com.ss.android.ugc.live&mcc_mnc=46000&cpu_support64=true&"
        f"host_abi=armeabi-v7a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_per"
        f"sonal_recommend=1&is_android_pad=0&ts={int(time.time())}&cdid=&md=0")
    data = {"user_ids": sec_user_id, "distribution_scenes": "183", "ad_type_flags": "0", "ad_white_flags": "0",
            "is_living": "1"}
    return path, data


async def get_live_room_by_map_path(city_code, max_time, did, iid):
    path = (f"/webcast/feed/?cate_id=0&channel_id=10&content_type=0&req_type=0&show_location=0&style=6"
            f"&sub_channel_id=0&sub_type=drawer_fresh&tab_id=11&type=live&device_id={did}&os_version=14.4"
            f"&webcast_sdk_version=1990&iid={iid}&app_name=aweme&pass-route=0&slide_guide_has_shown=1&"
            f"pass-region=0&webcast_gps_access=1&ac=WIFI&appTheme=light&js_sdk_version=2.7.0.6&"
            f"webcast_locale=zh-Hans_CN&effect_sdk_version=9.0.0&version_code=27.9.0&"
            f"vid=EFD43A02-A02C-4F29-B329-D6A867CF9AC3&channel=App%20Store&webcast_language=zh&is_vcd=1&"
            f"current_network_quality_info="
            f"&tma_jssdk_version=2.7.0.6&os_api=18&idfa=C423B28C-B4FC-485E-B384-42FD161CD2BD&device_platform=iphone&"
            f"device_type=iPhone%207&openudid=&build_number=158010&"
            f"minor_status=0&aid=1128&mcc_mnc=&screen_width=375&language=zh-Hans-CN&cdid="
            f"&app_version=15.8.0&enter_source=drawer_fresh-drawer_cover&live_source=live_small_picture&"
            f"req_from=enter_auto_from_room&city_code={city_code}&action=refresh")

    if max_time:
        path = (
            f"/webcast/feed/?cate_id=0&channel_id=10&content_type=0&req_type=0&show_location=0&style=6&sub_channel_id"
            f"=0&sub_type=drawer_fresh&tab_id=11&type=live&device_id={did}&os_version=14.4&"
            f"webcast_sdk_version=1990&iid={iid}&app_name=aweme&pass-route=0&"
            f"slide_guide_has_shown=1&pass-region=0&webcast_gps_access=1&ac=WIFI&appTheme=light&"
            f"js_sdk_version=2.7.0.6&webcast_locale=zh-Hans_CN&effect_sdk_version=9.0.0&version_code=27.9.0&"
            f"vid=&channel=App%20Store&webcast_language=zh&is_vcd=1&current_network_quality_info="
            f"&tma_jssdk_version=2.7.0.6&os_api=18&idfa=C423B28C-B4FC-485E-B384-42FD161CD2BD&device_platform=ipho"
            f"ne&device_type=iPhone%207&openudid=d2c0cc5d8436adaf0327dfd2eddf01cd8bdd1091&build_number=158010&mino"
            f"r_status=0&aid=1128&mcc_mnc=&screen_width=375&language=zh-Hans-CN&cdid=AC89061D-8F32-4A8C-BAEC-E6B723"
            f"0543ED&app_version=15.8.0&action=load_more&live_source=live_small_picture&req_from=drawer_fresh_loadmore"
            f"&enter_source=drawer_fresh-drawer_cover&cur_count=12&city_code={city_code}&max_time={max_time}")

    return path


async def medium_channel_feed_path(tag_id, install_time, refresh_index):
    if tag_id == "0":
        tag_id == ""
    path = (f"device_platform=webapp&aid=6383&channel=channel_pc_web&module_id=3003101&count=20&filterGids=&presented"
            f"_ids=&refresh_index=1&refer_id=&refer_type={refresh_index}&awemePcRecRawData=%7B%22is_xigua_user%22%3A0%2C%22is_cl"
            f"ient%22%3Afalse%7D&Seo-Flag=0&install_time={install_time}&tag_id={tag_id}&use_lite_type=1&xigua_user=0"
            f"&pc_client_type=1&pc_libra_divert=Windows&update_version_code=170400&support_h265=1&support_dash=1&versi"
            f"on_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_lang"
            f"uage=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=136.0.0.0&browser_online=true&engine_"
            f"name=Blink&engine_version=136.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platfor"
            f"m=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=")

    return path


async def aweme_board_path(board_type="0", board_sub_type="", device_data=None):
    if board_type == "0":
        path = (
            f"/aweme/v1/hot/search/list/?board_type={board_type}&board_sub_type&detail_list=1&need_board_tab=true&need_covid_tab=false&request_tag_from=h5&"
            f"iid={device_data['install_id']}&device_id={device_data['device_id']}&ac=wifi&channel=doutui_1128_android_101824&aid=1128&"
            f"app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=android&os=android&ssmix=a&device_"
            f"type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270901&resol"
            f"ution=1080*1920&dpi=480&update_version_code=27909900&_rticket=1746770901430&first_launch_timestamp=174107"
            f"0589&last_deeplink_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=n"
            f"ormal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&ts=17467"
            f"70901&cdid=")
    else:
        path = (
            f"/aweme/v1/hot/search/list/?board_type={board_type}&board_sub_type={board_sub_type}&detail_list=1&need_board_tab=false&need_covid_tab=false&request_tag_from=h5&"
            f"iid={device_data['install_id']}&device_id={device_data['device_id']}&ac=wifi&channel=doutui_1128_android_101824&aid=1128&"
            f"app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=android&os=android&ssmix=a&device_"
            f"type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270901&resol"
            f"ution=1080*1920&dpi=480&update_version_code=27909900&_rticket=1746770901430&first_launch_timestamp=174107"
            f"0589&last_deeplink_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=n"
            f"ormal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&ts=17467"
            f"70901&cdid=")

    return path


async def aweme_shorten_path(aweme_id, aweme_type="user", device_data=None):
    params = (
        f"/shorten/?iid={device_data['install_id']}&device_id={device_data['device_id']}&ac=wifi&channel=doutui_1128_android_101824&aid=1128&"
        f"app_name=aweme&version_code=270900&version_name=27.9.0&device_platform=android&os=android&ssmix=a&devic"
        f"e_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version=12&manifest_version_code=270901&re"
        f"solution=1080*1920&dpi=480&update_version_code=27909900&_rticket=1747877693718&first_launch_timestamp=17"
        f"41070589&last_deeplink_update_version_code=0&cpu_support64=true&host_abi=arm64-v8a&is_guest_mode=0&app_t"
        f"ype=normal&minor_status=0&appTheme=light&need_personal_recommend=1&is_android_pad=0&is_android_fold=0&"
        f"ts={int(time.time())}&cdid=22f8e095-3268-4124-83a1-c48311f498c7")
    domain = "https://www.iesdouyin.com/share/"
    if aweme_type == "mix":
        aweme_type = "mix/detail"
    if aweme_type == "live":
        aweme_type = "webcast/reflow"
        domain = "https://webcast.amemv.com/douyin/"
    data = {
        "targets": f"{domain}{aweme_type}/{aweme_id}?from_ssr=1&from_aid=1128&timestamp={int(time.time())}&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme",
        "belong": "aweme",
        "persist": "1"
    }

    return params, data


async def search_stream_path(keyword, count, offset, sort_type, publish_time, filter_duration, content_type):
    url = "https://www.douyin.com/aweme/v1/web/general/search/stream/"
    params = {
        "aid": "6383",
        "browser_language": "zh-CN",
        "browser_name": "Edge",
        "browser_online": "true",
        "browser_platform": "Win32",
        "browser_version": "142.0.0.0",
        "channel": "channel_pc_web",
        "cookie_enabled": "true",
        "count": count,
        "cpu_core_num": "12",
        "device_memory": "8",
        "device_platform": "webapp",
        "downlink": "10",
        "effective_type": "4g",
        "enable_history": "1",
        "engine_name": "Blink",
        "engine_version": "142.0.0.0",
        "from_group_id": "",
        "keyword": keyword,
        "list_type": "",
        "need_filter_settings": "1",
        "offset": offset,
        "os_name": "Windows",
        "os_version": "10",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "platform": "PC",
        "query_correct_type": "1",
        "round_trip_time": "100",
        "screen_height": "1440",
        "screen_width": "2560",
        "search_channel": "aweme_general",
        "search_source": "tab_search",
        "support_dash": "1",
        "support_h265": "1",
        "version_code": "190600",
        "version_name": "19.6.0",
        "webid": "",
    }
    if not sort_type == "0" or not publish_time == "0":
        params.update({
            "filter_selected": json.dumps({"sort_type": sort_type, "publish_time": publish_time}),
            "is_filter_search": "1"
        })

    if not content_type == "0" or not filter_duration == "":
        params.update({
            "filter_selected": json.dumps(
                {"sort_type": sort_type, "publish_time": publish_time, "content_type": content_type,
                 "filter_duration": filter_duration}),
            "is_filter_search": "1"
        })
    return url, params


async def week_select_path(term, next_page_ids=""):
    params = (f"/douyin/select/billboard/list/?luckydog_sdk_version=8.25.0-rc.3&luckydog_api_version=8.25.0-rc.3"
              f"&static_settings_version=60&dynamic_settings_version=60&polling_settings_version=0&ac=wifi&channel=dout"
              f"ui_1128_android_101824&aid=1128&app_name=aweme&version_code=270900&version_name=27.9.0&device_platform"
              f"=android&os=android&ssmix=a&device_type=SM-G9910&device_brand=samsung&language=zh&os_api=32&os_version"
              f"=12&manifest_version_code=270901&resolution=1080*1920&dpi=480&update_version_code=27909900&_rticket="
              f"1755504810182&first_launch_timestamp=1741070589&last_deeplink_update_version_code=27909900&cpu_support"
              f"64=true&host_abi=arm64-v8a&is_guest_mode=0&app_type=normal&minor_status=0&appTheme=light&need_personal"
              f"_recommend=1&is_android_pad=0&is_android_fold=0&ts=1755504809&cdid=22f8e095-3268-4124-83a1-c48311f498c7"
              f"&rom=SAMSUNG&has_alipay=0&p_switch=1&rom_version=unknown&luckycat_version_name=8.25.0-rc.3&luckycat_v"
              f"ersion_code=890100&lucky_is_32=0&lucky_device_score=10.0&lucky_device_type=SM-G9910&status_bar_height=24"
              f"&request_tag_from=lynx&board_type=0&next_page_ids={next_page_ids}&only_directory=false&term={term}&entrance_type="
              f"1128_activity_weekly_page_im")

    if not next_page_ids == "":
        params += f"&rt=1"
    else:
        params += f"&rt=0"
    return params



async def index_feed_path(refresh_index):
    params = ('/aweme/v1/web/tab/feed/?device_platform=webapp&aid=6383&channel=channel_pc_web&tag_id&live_insert_type&'
              f'count=10&refresh_index={refresh_index}&'
              'video_type_select=1&aweme_pc_rec_raw_data={"newVideoPrefer":{"fsn":[],"min":[],'
              '"show":[],"skip":[],"head":[]},"is_client":false,"ff_danmaku_status":1,"danmaku_switch_status":0,"is_dash_user":1,'
              '"related_recommend":1,"is_xigua_user":0}&globalwid&min_window=0&free_right=0&view_count=0&'
              'plug_block=0&ug_source&creative_id&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1'
              '&webcast_sdk_version=170400&webcast_version_code=170400&version_code=170400&version_name=17.4.0&cookie_'
              'enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser'
              '_name=Chrome&browser_version=141.0.0.0&browser_online=true&engine_name=Blink&engine_version=141.0.0.0&o'
              's_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&'
              'round_trip_time=50')


    if refresh_index == "1":
        params = params +"&pull_type=0"
    else:
        params = params + "&pull_type=2"

    return params
