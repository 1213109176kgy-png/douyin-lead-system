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
@File    ：core.py
@IDE     ：PyCharm 
@Author  ：  
@Date    ：2024/11/15 13:35 
@WebSite ：
'''
import re

from core import CustomException, json_success_response
from libs import get_request_proxy


class BaseLemon:
    def __init__(self, request):
        self.request = request
        self.headers = {
            'sdk-version': '2',
            'passport-sdk-version': '20358',
            'x-vc-bdturing-sdk-version': '2.2.1.i18n',
            'x-tt-store-idc': 'useast5',
            'x-tt-store-region': 'us',
            'x-tt-store-region-src': 'did',
            'User-Agent': 'com.bd.nproject/23020 (Linux; U; Android 12; zh_CN; 22021211RC; Build/V417IR;tt-ok/3.10.0.2)',
            'Host': 'api22-normal-useast1a.lemon8-app.com',
            'Connection': 'Keep-Alive',
            'Accept': '*/*',
            'Cache-Control': 'no-cache'
        }

    async def get_aweme_id(self, share_text, proxy):
        try:
            aweme_id = re.search(r'/(\d+)\?', share_text).group(1)
            if aweme_id:
                return aweme_id
        except:
            pass

        res = await self.request.app.ctx.curl_client.http_get(share_text, allow_redirects=False, proxy=proxy)
        location = res.headers['location']
        try:
            aweme_id = re.search(r'/(\d+)\?', location).group(1)
        except:
            aweme_id = None
        return aweme_id

    async def get_user_id(self, share_text, proxy):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/125.0.0.0',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': 'www.lemon8-app.com',
            'Connection': 'keep-alive'
        }
        try:
            res = await self.request.app.ctx.curl_client.http_get(share_text, proxy=proxy)
            res_location = res.headers.get('location')
            response = await self.request.app.ctx.curl_client.http_get(res_location, headers=headers, proxy=proxy)
            response_text = response.text
            match = re.search(r'"enterPageId":"(\d+)"', response_text).group(1)

            return match
        except Exception as e:
            return None

    async def __get_proxy(self):
        return await get_request_proxy(self.request, proxy_type="overseas")

    async def aweme_detail(self, data):
        """
        https://www.lemon8-app.com/ilovemyself526/7328978388428898821?language=en&region=en&ui_language=en&user_id=7379163877194138629
        """
        aweme_id = data.get('aweme_id', None)
        share_text = data.get('share_text', None)  # https://v.lemon8-app.com/al/xUdYUYspR
        proxy = await self.__get_proxy()
        if not aweme_id:
            if not share_text:
                raise CustomException()
            aweme_id = await self.get_aweme_id(share_text, proxy)
            if not aweme_id:
                raise CustomException()
        url = f"https://api22-normal-useast1a.lemon8-app.com/api/230/article/info?group_id={aweme_id}&item_id={aweme_id}&from_category=0&context=1&gender=null&aggr_type=0&youtube=1&manifest_version_code=230&app_version=2.3.0&original_channel=gp&channel=gp&device_type=22021211RC&language=ja&app_version_minor=2.3.0&resolution=1920%2A1080&update_version_code=23020&sys_language=zh&sys_region=CN&os_api=32&tz_name=Asia%2FShanghai&tz_offset=28800&logo=topbuzz&dpi=480&app_id=2657&brand=Redmi&ac=wifi&os=android&mcc_mnc=46000&os_version=12&hevc_supported=1&version_code=230&cold_start=0&release_build=v2.3.0-gp-51d17aaa&sim_oper=460000&version_name=2.3.0&device_brand=Redmi&device_platform=android&sim_region=cn&region=jp&aid=2657&ui_language=en"
        response = await self.request.app.ctx.curl_client.http_get(url, headers=self.headers, proxy=proxy)
        return json_success_response(data=response.json())

    async def user_detail(self, data):
        user_id = data.get('user_id', None)
        share_text = data.get('share_text', None)
        proxy = await self.__get_proxy()

        if not user_id:
            if not share_text:
                raise CustomException()
            user_id = await self.get_user_id(share_text, proxy)
            if not user_id:
                raise CustomException()
        url = f"https://api22-normal-useast1a.lemon8-app.com/api/230/user/profile/homepage?user_id={user_id}&youtube=1&manifest_version_code=230&app_version=2.3.0&original_channel=gp&channel=gp&device_type=22021211RC&language=ja&app_version_minor=2.3.0&resolution=1920*1080&update_version_code=23020&sys_language=zh&sys_region=CN&os_api=32&tz_name=Asia%2FShanghai&tz_offset=28800&logo=topbuzz&dpi=480&app_id=2657&brand=Redmi&ac=wifi&os=android&mcc_mnc=46000&os_version=12&hevc_supported=1&version_code=230&cold_start=0&release_build=v2.3.0-gp-51d17aaa&sim_oper=460000&version_name=2.3.0&device_brand=Redmi&device_platform=android&sim_region=cn&region=jp&aid=2657&ui_language=en"
        response = await self.request.app.ctx.curl_client.http_get(url, headers=self.headers, proxy=proxy)
        return json_success_response(data=response.json())

    async def user_post(self, data):
        user_id = data.get('user_id', None)
        share_text = data.get('share_text', None)
        max_behot_time = data.get('max_behot_time', "")
        proxy = await self.__get_proxy()

        if not user_id:
            if not share_text:
                raise CustomException()
            user_id = await self.get_user_id(share_text, proxy)
            if not user_id:
                raise CustomException()
        url = f"https://api22-normal-useast1a.lemon8-app.com/api/230/stream?category=486&count=20&first_request=0&session_impr_id=0&tab=general&max_behot_time={max_behot_time}&category_parameter={user_id}&mode=comment_in_feed&youtube=1&manifest_version_code=230&app_version=2.3.0&original_channel=gp&channel=gp&device_type=22021211RC&language=ja&app_version_minor=2.3.0&resolution=1920*1080&update_version_code=23020&sys_language=zh&sys_region=CN&os_api=32&tz_name=Asia%2FShanghai&tz_offset=28800&logo=topbuzz&dpi=480&app_id=2657&brand=Redmi&ac=wifi&os=android&mcc_mnc=46000&os_version=12&hevc_supported=1&version_code=230&cold_start=0&release_build=v2.3.0-gp-51d17aaa&sim_oper=460000&version_name=2.3.0&device_brand=Redmi&device_platform=android&sim_region=cn&region=jp&aid=2657&ui_language=en"
        response = await self.request.app.ctx.curl_client.http_get(url, headers=self.headers, proxy=proxy)
        return json_success_response(data=response.json())
