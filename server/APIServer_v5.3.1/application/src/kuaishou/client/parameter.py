#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：parameter.py
@IDE     ：PyCharm 

@Date    ：2025/4/19 10:00 
'''
import random

from core import get_device_data
from libs.common import generate_random_string_alph

base_url = "https://www.kuaishou.com/graphql"
home_url = "https://www.kuaishou.com/?isHome=1"


async def aweme_detail_headers():
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/129.0.0.0",
    }
    return headers


async def base_headers(cookie: str, referer: str):
    data = {
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'accept': '*/*',
        'content-type': 'application/json',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    if cookie:
        data['Cookie'] = cookie
    return data


async def base_user_post(user_id: str, pcursor: str = ""):
    data = {"operationName": "visionProfilePhotoList",
            "variables": {"userId": user_id, "pcursor": pcursor, "page": "profile"},
            "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}
    return data


async def base_user_info(user_id: str):
    data = {"operationName": "visionProfile", "variables": {"userId": user_id},
            "query": "query visionProfile($userId: String) {\n  visionProfile(userId: $userId) {\n    result\n    hostName\n    userProfile {\n      ownerCount {\n        fan\n        photo\n        follow\n        photo_public\n        __typename\n      }\n      profile {\n        gender\n        user_name\n        user_id\n        headurl\n        user_text\n        user_profile_bg_url\n        __typename\n      }\n      isFollowing\n      __typename\n    }\n    __typename\n  }\n}\n"}
    return data


async def search_video_data(keyword: str, pcursor: str):
    data = {"operationName": "visionSearchPhoto",
            "variables": {"keyword": keyword, "pcursor": pcursor, "page": "search",
                          "searchSessionId": "MTRfMF8xNzE3NzI1MjAwMzU1X-WMl-S6rF83OTMy"},
            "query": "fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"}
    return data


async def aweme_v2_headers(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Host": "www.kuaishou.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": cookie
    }
    return headers

async def app_headers():
    headers = {
        'Host': 'txjp.gifshow.com',
        'Connection': 'keep-alive',
        'User-Agent': 'kwai-android aegon/3.10.0',
        'Accept-Language': 'en-us',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Client-Info': 'model=MI 9;os=Android;nqe-score=1;network=WIFI;signal-strength=4;',
    }
    return headers


async def aweme_detail_path(app, photo_ids):
    did_data = await get_device_data(app=app, device_type="k_egid")
    did = f"ANDROID_{await generate_random_string_alph(16)}"
    egid = did_data['device_token']
    url = f"https://txjp.gifshow.com/rest/n/photo/info2?earphoneMode=1&mod=Xiaomi(MI%209)&appver=10.5.40.26392&isp=&language=en-us&ud=0&did_tag=0&egid={egid}&thermal=10000&net=WIFI&kcv=1577&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=&android_os=0&boardPlatform=msmnile&kpn=KUAISHOU&androidApiLevel=30&newOc=ALI_CPD%2C666&slh=0&country_code=vn&nbh=44&hotfix_ver=&did_gt=1730269438691&keyconfig_state=2&cdid_tag=0&sys=ANDROID_11&max_memory=256&cold_launch_time_ms=1730269784485&oc=ALI_CPD%2C666&sh=2340&ddpi=440&deviceBit=0&browseType=4&socName=Qualcomm%20Snapdragon%208150&is_background=0&c=ALI_CPD%2C666&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5499&grant_browse_type=AUTHORIZED&iuid=&rdid=&sbh=75&darkMode=false&did={did}"
    payload = 'photoInfos=' + photo_ids + '&cs=false&client_key=3c2cd3f3&os=android&client_key=3c2cd3f3&uQaTag='
    return url, payload


async def aweme_comment_path(photo_id, pcursor):
    did = f"ANDROID_{await generate_random_string_alph(16)}"
    url = f"https://apijs.ksapisrv.com/rest/n/comment/list/v2?mod=vivo%28V1923A%29&appver=10.2.30.24518&isp=CMCC&language=zh-cn&ud=0&did_tag=3&egid=&net=WIFI&kcv=1507&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.2&android_os=0&boardPlatform=aosp-user&kpn=KUAISHOU&androidApiLevel=28&newOc=GENERIC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1689391458407&keyconfig_state=2&sys=ANDROID_9&max_memory=192&cold_launch_time_ms=1689391935860&oc=GENERIC&sh=1600&app_status=3&ddpi=240&deviceBit=0&browseType=4&power_mode=0&socName=Qualcomm%20MSM8998&is_background=0&c=GENERIC&sw=900&ftt=&abi=arm32&userRecoBit=0&device_abi=arm64&totalMemory=3946&grant_browse_type=AUTHORIZED&iuid=&sbh=36&darkMode=false"
    payload = f'photoId={photo_id}&order=public&pcursor={pcursor}&count=10&photoPageType=0&enableEmotion=true&expTag=1_u%2F2002346804362896866_bs6505&urlPackagePage2=FEATURED_PAGE&ptp=CgFAEgLqARoClgg%3D&os=android&cs=false&sig=cdc45f0517a77f5682c08103315c2ee9&client_key=3c2cd3f3&uQaTag=&__NS_sig3=574636159d99fc327b1f1c1df69a05dd2512b661020e0016'
    return url, payload


async def aweme_sub_comment_path(photo_id,root_comment_id, pcursor):
    did = f"ANDROID_{await generate_random_string_alph(16)}"
    url = f"https://apijs2.gifshow.com/rest/n/comment/sublist?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid=DFPE4EC61603B3D46D661561FF1AAE7440705EE06876EE308C02F1B57DAB6CA2&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1745631748951&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=ANDROID_76428f243b739b06&sbh=72&darkMode=false&did=ANDROID_2eee6805b359a140"
    payload = f'photoId={photo_id}&order=desc&pcursor={pcursor}&rootCommentId={root_comment_id}&enableEmotion=true&ptp=CgEBEgLsARoF%2F%2F%2F%2F%2Fw8%3D&count=10&os=android&token=&client_salt=&cs=false&client_key=3c2cd3f3&kuaishou.api_st=Cg9rdWFpc2hvdS5hcGkuc3QSoAFIwzT70gSebAVhrDNzxWJCpGKr8YQdeSfuhhmHrXYOB05bpEeNn-eRU-2j_GIXCl2dI4SSgPt9D7sTCvdxa_ONyeBgH49TN-zQHVcXcO9v_wVP4BBEWK8ISZUe_Pt01gtN3hGajd0-bmXLrQC0Dg0fe1k6DuxQUIEyd0w-LRv9jh2KdrFngnLvWmaUQhpZ9f3KGDjdyzjWBefhgg8ULO3eGhIUM110NdJDN4QHnTx2pK5v0IIiIJzts8E6g2_JvhFnknXU6-5qNdW4pGTv5zO2GDvznnl1KAUwAQ&uQaTag=&sig=2051f25cb16539da160f762b45b4ac63&__NStokensig=c27113199339dd5731451c69a64f93b757b8ad44b4b5ecd386764e19c4636ef3&__NS_sig3=425323004ed15a30490a09085cfc918f27281d78161b1503'
    return url, payload


async def user_info_v3_path(app,user_id):
    did_data = await get_device_data(app=app,device_type="k_egid")
    did = did_data['device_id_str']
    egid = did_data['device_token']
    url = f"https://apijs2.ksapisrv.com/rest/n/user/profile/v2?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid={egid}&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1758250160132&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=ANDROID_76428f243b739b06&sbh=72&darkMode=false&did={did}"
    payload = f'user={user_id}&pv=true&scene=5&version=2&source=DEFAULT&cs=false&client_key=3c2cd3f3&os=android&kuaishou.api_st=&uQaTag=&token=-73828320&client_salt=&__NStokensig=&sig=&__NS_sig3='
    return url, payload



async def user_post_app_path(app, user_id, pcursor):
    did_data = await get_device_data(app=app, device_type="k_egid")
    did = did_data['device_id_str']
    egid = did_data['device_token']
    url = f"https://az4-api.ksapisrv.com/rest/n/feed/profile2?earphoneMode=1&mod=vivo%28V2238A%29&appver=13.1.40.40682&isp=&language=zh-cn&ud=4038716990&did_tag=0&egid={egid}&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=13.1&android_os=0&oDid=ANDROID_d00d8a7f3a1554d1&boardPlatform=vivo&kpn=KUAISHOU&newOc=ALI_CPD%2C666&androidApiLevel=32&slh=0&country_code=CN&nbh=0&hotfix_ver=&did_gt=1757298783655&keyconfig_state=2&cdid_tag=2&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1757298755291&oc=ALI_CPD%2C666&sh=1920&deviceBit=0&browseType=4&ddpi=480&socName=UNKNOWN&is_background=0&c=ALI_CPD%2C666&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=arm64&icaver=1&totalMemory=3939&grant_browse_type=AUTHORIZED&iuid=&rdid=ANDROID_edf7887be7b1b4ee&sbh=72&darkMode=false&did={did}"
    payload = f"user_id={user_id}&pcursor={pcursor}&lang=zh&count=9&privacy=public&referer=ks%3A%2F%2Fprofile%2F1875376602%2F5230086710386007523%2Fnull&displayType=3&teenagerMode=false&tubeCustomParams=%7B%22tubeCardABParam%22%3A1%7D&preRequest=false&sourcePhotoPage=bs&profileRequestTag=&profileFeedExtraInfo=%7B%22enableGuestPreview%22%3Afalse%7D&videoModelCrowdTag=&os=android&token=&cs=false&client_key=3c2cd3f3"
    return url, payload

async def short_link_path(app, photo_id):
    did_data = await get_device_data(app=app, device_type="k_egid")
    did = did_data['device_id_str']
    egid = did_data['device_token']
    url = f"https://api.kuaishouzt.com/rest/zt/share/any?gid={egid}&mod=Redmi%2822021211RC%29&appver=10.5.40.26392&cdid_tag=0&language=zh-cn&sys=ANDROID_12&mcc=460000&did_tag=0&countryCode=cn&net=WIFI&socName=Unknown&kpf=ANDROID_PHONE&ver=10.5&c=ANDROID_SHENMA_ZW_SSYQ_CPC&oDid=ANDROID_{did}&android_os=0&os=android&boardPlatform=Redmi&ftt=&kpn=KUAISHOU&androidApiLevel=32&abi=arm32&device_abi=arm64&memoryTotalSize=5949&rdid=ANDROID_{did}&did=ANDROID_{did}"
    payload = f'kpf=ANDROID_PHONE&shareMethod=&subBiz=BROWSE_SLIDE_PHOTO&kpn=KUAISHOU&shareResourceType=PHOTO_OTHER&extTransientParams=%7B%7D&extRecoParams=%7B%7D&shareChannelId=COPY_LINK&shareMode=&shareChannel=copyLink&sdkVersion=1.14.0.4&theme=light&kuaishou.api_st=&shareObjectId={photo_id}'
    return url, payload


async def user_short_link_path(app, user_id):
    did_data = await get_device_data(app=app, device_type="k_egid")
    did = did_data['device_id_str']
    egid = did_data['device_token']
    url = f"https://api.kuaishouzt.com/rest/zt/share/any?gid={egid}&mod=Xiaomi%282206123SC%29&appver=10.5.40.26392&cdid_tag=0&language=zh-cn&sys=ANDROID_12&mcc=460000&did_tag=0&countryCode=cn&net=WIFI&socName=Unknown&kpf=ANDROID_PHONE&ver=10.5&c=ALI_CPD%2C666&oDid=ANDROID_b6046e08c768d0d9&android_os=0&os=android&boardPlatform=Xiaomi&ftt&kpn=KUAISHOU&androidApiLevel=32&abi=arm32&device_abi=arm64&userId=73828320&memoryTotalSize=5949&rdid=ANDROID_913294289a3d477a&did={did}"
    payload = f'kpf=ANDROID_PHONE&shareMethod=&subBiz=PROFILE&kpn=KUAISHOU&shareResourceType=PROFILE_OTHER&extTransientParams=&token=&extRecoParams=%7B%7D&shareChannelId=COPY_LINK&shareMode=&shareChannel=copyLink&sdkVersion=1.14.0.4&theme=light&shareObjectId={user_id}'
    return url, payload




async def hot_billboard_v2_path(board_type):
    url = "https://apijs1.gifshow.com/rest/n/hot/board?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid=&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1752478421120&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=&sbh=72&darkMode=false&did="
    if board_type == "1":
        payload = "boardId=1&boardType=1&count=50&cs=false&client_key=3c2cd3f3&os=android"
    elif board_type == "2":
        payload = "boardId=6&boardType=4&count=50&cs=false&client_key=3c2cd3f3&os=android"
    elif board_type == "3":
        payload = "boardId=7&boardType=5&count=50&cs=false&client_key=3c2cd3f3&os=android"
    elif board_type == "4":
        payload = "boardId=8&boardType=6&count=50&cs=false&client_key=3c2cd3f3&os=android"
    elif board_type == "5":
        url = "https://apijs1.gifshow.com/rest/n/tag/leaderboard?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid=&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1752478421120&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=&sbh=72&darkMode=false&did="
        payload = "phase=26&categoryId=26&cs=false&client_key=3c2cd3f3&os=android"
    elif board_type == "6":
        url = "https://apijs1.gifshow.com/rest/n/search/home?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid=&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1752478421120&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=&sbh=72&darkMode=false&did="
        payload = "configType=4&needConfig=false&pageSource=0&dataTypes=17&extParams={}&os=android&client_salt=&cs=false&client_key=3c2cd3f3"
    else:
        url = "https://apijs1.gifshow.com/rest/n/hot/board?earphoneMode=1&mod=OPPO%28PGAM10%29&appver=10.5.40.26392&isp=CMCC&language=zh-cn&ud=73828320&did_tag=0&egid=&thermal=10000&net=WIFI&kcv=1599&app=0&kpf=ANDROID_PHONE&bottom_navigation=false&ver=10.5&oDid=ANDROID_2eee6805b359a140&android_os=0&boardPlatform=OPPO&kpn=KUAISHOU&androidApiLevel=32&newOc=ANDROID_SHENMA_ZW_SSYQ_CPC&slh=0&country_code=cn&nbh=0&hotfix_ver=&did_gt=1742355571976&keyconfig_state=2&cdid_tag=0&sys=ANDROID_12&max_memory=192&cold_launch_time_ms=1752478421120&oc=ANDROID_SHENMA_ZW_SSYQ_CPC&sh=1920&ddpi=480&deviceBit=0&browseType=4&socName=Unknown&is_background=0&c=ANDROID_SHENMA_ZW_SSYQ_CPC&sw=1080&ftt=&abi=arm32&userRecoBit=0&device_abi=&totalMemory=5949&grant_browse_type=AUTHORIZED&iuid=&rdid=&sbh=72&darkMode=false&did="
        payload = "boardId=1&boardType=1&count=50&cs=false&client_key=3c2cd3f3&os=android"
    return url, payload



