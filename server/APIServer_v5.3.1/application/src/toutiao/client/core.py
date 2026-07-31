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
@Date    ：2024/11/15 11:48 
@WebSite ：
'''
import re
import time

from sanic import Request, HTTPResponse
from sanic.views import HTTPMethodView

from application.src.toutiao.args.abogus import ABogus
from application.src.toutiao.args.x_gorgons import splitParams, X_Gorgon0404
from core import get_device_data, json_success_response, CustomException
from libs.common import generate_random_string, generate_random_string_alph, get_domain_from_url
from libs.request import get_request_data, get_request_proxy


class BaseView(HTTPMethodView):
    """
    视图的基类
    """
    handler_method = ''

    async def post(self, request: Request) -> HTTPResponse:
        data = await get_request_data(request)
        handler = CoreHandler(request)
        handler_method = getattr(handler, self.handler_method)
        return await handler_method(data)


class CoreHandler:
    """
    处理详情的类
    """

    def __init__(self, request):
        self.request = request

    async def extract_id(self, share_text):
        link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          share_text.replace("#", ""))
        if not link:
            return None
        url = link[0]
        match = re.search(r'/(\d{1,20})/', url)
        if match:
            return match.group(1)
        else:
            locations = await self.request.app.ctx.curl_client.http_get(url, allow_redirects=True)
            url = str(locations.url)
            match = re.search(r'/(\d{1,20})/', url)
            if match:
                return match.group(1)
            return None

    async def _get_device_data(self):
        data = await get_device_data(self.request.app)
        return data

    async def process_a_bogus(self, params, ua):
        ab = ABogus(user_agent=ua)
        a_bogus = await ab.get_value(params)
        return f"{params}&a_bogus={a_bogus}"

    async def _get_device(self):
        device_data = await self._get_device_data()
        return device_data

    async def _get_app_params(self, url, device_data):
        params_str = splitParams(url)
        cookies = (
            f"sessionid={await generate_random_string(32)};"
            f"store-region=cn-ah; store-region-src=did; "
            f"install_id={device_data['install_id_str']}; ttreq=1${await generate_random_string(40)}; "
            f"odin_tt={await generate_random_string_alph(160)}"
        )
        xgorgon = X_Gorgon0404(params_str, '', '')
        headers = {
            'X-SS-REQ-TICKET': str(round(time.time() * 1000)),
            'X-Gorgon': xgorgon.get('X-Gorgon'),
            'X-Khronos': xgorgon.get('X-Khronos'),
            'sdk-version': '2',
            'Accept-Encoding': 'gzip',
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; 22021211RC Build/V417IR) NewsArticle/8.4.2 tt-ok/3.10.0.2",
            'Cookie': cookies,
            'Host': await get_domain_from_url(url),
            'Connection': 'Keep-Alive',
        }
        return headers

    async def fetch_detail(self, url_template, aweme_id, data=None):
        device_data = await self._get_device()
        if 'count' in data:
            url = url_template.format(
                aweme_id=aweme_id,
                install_id_str=device_data['install_id'],
                device_id_str=device_data['device_id'],
                count=data['count'],
                offset=data['offset'],
                behot_time=data['behot_time'],
            )
        else:
            url = url_template.format(
                aweme_id=aweme_id,
                install_id_str=device_data['install_id'],
                device_id_str=device_data['device_id']
            )

        try:
            response = await self.request.app.ctx.curl_client.http_get(url, headers=await self._get_app_params(url=url,
                                                                                                               device_data=device_data),
                                                                       proxy=await get_request_proxy(self.request))
            data = response.json()
            return json_success_response(data)
        except Exception as e:
            raise e

    async def _get_request_params(self, data):
        aweme_id = data.get('aweme_id') or data.get('user_id')
        share_text = data.get('share_text')
        if not aweme_id:
            if not share_text:
                raise CustomException()
            aweme_id = await self.extract_id(share_text) or None
            if not aweme_id:
                raise CustomException()
        return aweme_id

    async def handle_detail(self, data, url_template):
        aweme_id = await self._get_request_params(data)
        return await self.fetch_detail(url_template, aweme_id, data)

    async def video_detail(self, data):
        url_template = (
            'https://api5-normal.toutiaoapi.com/video/app/article/information/v25/'
            '?group_id={aweme_id}&item_id={aweme_id}&aggr_type=1&context=1&flags=64&from_category=__all__&'
            'article_page=1&ad_download=%7B%7D&video_detail_type=1&client_extra_params=%7B%22playparam%22%3A%22'
            'codec_type%3A7%2Cresolution%3A1080*1920%2Ccdn_type%3A6%2Cunwatermark%3A1%22%2C%22disable_commerce_ads'
            '%22%3A%220%22%7D&iid={install_id_str}&device_id={device_id_str}&ac=wifi&'
            'mac_address=&channel=lite2_tengxun&aid=35&app_name=news_article_lite&version_code=842&version_name=8.4.2&'
            'device_platform=android&ab_version=668905%2C9273949%2C1859937%2C668903%2C9273988%2C5315659%2C8833288%2C'
            '9153040%2C9325113%2C668908%2C9273999%2C668907%2C9273985%2C668906%2C9273950%2C668904%2C9273968%2C668776%'
            '2C9274006%2C9207338%2C9101858%2C8935762%2C9029148%2C9093830%2C9109302%2C9288554%2C9304121%2C9343863&ab_'
            'client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=z1&abflag=3&ssmix=a&device_type=22021211RC&device_brand=Redmi&'
            'language=zh&os_api=32&os_version=12&openudid=&manifest_version_code=8420&resolution=1080*1920&dpi=480&'
            'update_version_code=84208&_rticket=1719307027431&sa_enable=0&dq_param=0&plugin_state=&session_id=&host_'
            'abi=armeabi-v7a&rom_version=32&cdid='
        )
        return await self.handle_detail(data, url_template)

    async def video_detail_v2(self, data):
        aweme_id = await self._get_request_params(data)
        device_data = await self._get_device()

        url = (
            f"https://api5-normal.toutiaoapi.com/ugc/video/v1/aweme/detail/info/?_rticket={round(time.time() * 1000)}&manifest_vers"
            f"ion_code=8480&iid={device_data['install_id']}&channel=tengxun3&isTTWebView=0&device_type=22021211RC&language=zh&h"
            f"ost_abi=armeabi-v7a&resolution=1080*1920&uuid=866084040106293&openudid=be2ed3deb0633656&update_versi"
            f"on_code=84807&dq_param=0&cdid=9098d6aa-e330-483c-9148-5ac73cb665eb&dpi=480&ac=wifi&os=android&device"
            f"_id={device_data['device_id']}&os_version=12&version_code=848&tma_jssdk_version=2.14.0.8&app_name=news_article"
            f"&version_name=8.4.8&plugin=0&device_brand=Redmi&ssmix=a&device_platform=android&aid=13&rom_version=32")

        post_data = {
            "group_id": aweme_id,
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "_rticket": round(time.time() * 1000),
            "cdid": "9098d6aa-e330-483c-9148-5ac73cb665eb",
            "channel": "tengxun3",
            "aid": "13",
            "app_name": "news_article",
            "version_code": "848",
            "version_name": "8.4.8",
            "manifest_version_code": "8480",
            "update_version_code": "84807",
            "resolution": "1080*1920",
            "dpi": "480",
            "device_type": "22021211RC",
            "device_brand": "Redmi",
            "language": "zh",
            "os_api": "32",
            "os_version": "12",
            "ac": "wifi",
            "dq_param": "0",
            "plugin": "0",
            "isTTWebView": "0",
            "host_abi": "armeabi-v7a",
            "tma_jssdk_version": "2.14.0.8",
            "rom_version": "32",
            "iid": device_data['install_id'],
            "device_id": device_data['device_id'],
            "openudid": "",
            "uuid": ""
        }

        try:
            response = await self.request.app.ctx.curl_client.http_post(url, headers=await self._get_app_params(url=url,
                                                                                                                device_data=device_data),
                                                                        data=post_data,
                                                                        proxy=await get_request_proxy(self.request))
            data = response.json()
            return json_success_response(data)
        except Exception as e:
            raise e

    async def article_detail(self, data):
        url_template = (
            'https://lf3-article.toutiaostatic.com/article/content/lite/17/1/{aweme_id}/{aweme_id}/1/?iid={install_id_str}&device_id={device_id_str}&ac=wifi&channel=lite2_tengxun&aid=35&app_name=news_article_lite&version_code=842&version_name=8.4.2&device_platform=android&ab_version=668905%2C9273949%2C1859937%2C668903%2C9273988%2C5315659%2C8833288%2C9153040%2C9325113%2C668908%2C9273999%2C668907%2C9273985%2C668906%2C9273950%2C668904%2C9273968%2C668776%2C9274006%2C9207338%2C9101858%2C8935762%2C9029148%2C9093830%2C9109302%2C9288554%2C9304121%2C9343863&ab_client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=z1&abflag=3&ssmix=a&device_type=22021211RC&device_brand=Redmi&language=zh&os_api=32&os_version=12&manifest_version_code=8420&resolution=1080*1920&dpi=480&update_version_code=84208&_rticket=1719308554501&sa_enable=0&dq_param=0&plugin_state=69312443478045&session_id=14f884ba-af7f-49f5-a6ea-461b485317fa&host_abi=armeabi-v7a&rom_version=32&cdid=e86cb5de-89c2-40e4-bf6e-517c48b894e8'
        )
        return await self.handle_detail(data, url_template)

    async def article_root_comment(self, data):
        offset = data.get('offset', 0)
        url_template = (
            f'https://api5-normal-lf.toutiaoapi.com/article/v4/tab_comments/?fold=1&offset={offset}&group_id={{aweme_id}}&count=20&comment_request_from=1&category=thread_aggr&iid={{install_id_str}}&device_id={{device_id_str}}&ac=wifi&channel=lite7_wandoujia&aid=35&app_name=news_article_lite&version_code=862&version_name=8.6.2&device_platform=android&os=android&ab_version=4113875%2C4522570%2C4890007%2C5361616%2C5578387%2C6034695%2C6571804%2C7028329%2C7204588%2C7237725%2C7354844%2C7551466%2C7670551%2C7673030%2C7681479%2C8087081%2C8160323%2C8186512%2C8426872%2C8512477%2C8553215%2C8611793%2C8639938%2C8663350%2C8721367%2C8759025%2C8760183%2C8779946%2C8885971%2C9023653%2C9023668%2C9044860%2C9067502%2C9183639%2C9262164%2C9408359%2C9568459%2C9568604%2C9645152%2C9671603%2C9685161%2C9704858%2C9723956%2C9729417%2C9766390%2C9766562%2C9766718%2C9766878%2C9767011%2C9767241%2C9811660%2C9830639%2C9858014%2C9880692%2C9939975%2C9941241%2C10025069%2C10034133%2C10036483%2C10103595%2C10113003%2C10117535%2C10136567%2C10145535%2C10146301%2C10149105%2C10161949%2C10171385%2C10172345%2C10178159%2C10179498%2C10180362%2C10183118%2C10183229%2C10184513%2C10187546%2C10236938%2C10242931%2C10251872%2C10260657%2C10266242%2C10276670%2C10279081%2C10300338%2C10300454%2C10301078%2C10311511%2C10328296%2C10329430%2C10336462%2C10336473%2C10336987%2C10342315%2C10351429%2C10352297%2C10365307%2C10370756%2C668906%2C9960584%2C10344507%2C10364834%2C668905%2C10344506%2C668904%2C10344522%2C668903%2C10344537%2C668776%2C10344552%2C10307730%2C10345633%2C10351259%2C668907%2C9837813%2C10344534%2C668908%2C10344548%2C1859936%2C5315659%2C9153040%2C9259782%2C10234669%2C9101858%2C10139069%2C7142413%2C8504307%2C8612126%2C9751406%2C9758710%2C10049555%2C9416947%2C9470968%2C9797523%2C10036512%2C10068099%2C10102443%2C10105788%2C10196525%2C10289988&ab_client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=PGAM10&device_brand=OPPO&language=zh&os_api=32&os_version=12&manifest_version_code=8620&resolution=1080*1920&dpi=480&update_version_code=86211&_rticket=1728537258848&sa_enable=0&dq_param=0&plugin_state=280419485511709&session_id=7648f3f6-34a8-40b0-871b-feef2e7ce106&host_abi=armeabi-v7a&tma_jssdk_version=2.8.0.14&rom_version=coloros__v417ir+release-keys&cdid=71199617-caa9-4030-9ea7-29ac881ce189'
        )
        return await self.handle_detail(data, url_template)

    async def article_sub_comment(self, data):
        offset = data.get('offset', 0)
        root_comment_id = data.get('root_comment_id', '')
        url_template = (
            f'https://api5-normal-lf.toutiaoapi.com/2/comment/v4/reply_list/?offset={offset}&group_id={{aweme_id}}&count=20&id={root_comment_id}&simple_stick_reply_id={root_comment_id}&iid={{install_id_str}}&device_id={{device_id_str}}&ac=wifi&channel=lite7_wandoujia&aid=35&app_name=news_article_lite&version_code=862&version_name=8.6.2&device_platform=android&os=android&ab_version=4113875%2C4522570%2C4890007%2C5361616%2C5578387%2C6034695%2C6571804%2C7028329%2C7204588%2C7237725%2C7354844%2C7551466%2C7670551%2C7673030%2C7681479%2C8087081%2C8160323%2C8186512%2C8426872%2C8512477%2C8553215%2C8611793%2C8639938%2C8663350%2C8721367%2C8759025%2C8760183%2C8779946%2C8885971%2C9023653%2C9023668%2C9044860%2C9067502%2C9183639%2C9262164%2C9408359%2C9568459%2C9568604%2C9645152%2C9671603%2C9685161%2C9704858%2C9723956%2C9729417%2C9766390%2C9766562%2C9766718%2C9766878%2C9767011%2C9767241%2C9811660%2C9830639%2C9858014%2C9880692%2C9939975%2C9941241%2C10025069%2C10034133%2C10036483%2C10103595%2C10113003%2C10117535%2C10136567%2C10145535%2C10146301%2C10149105%2C10161949%2C10171385%2C10172345%2C10178159%2C10179498%2C10180362%2C10183118%2C10183229%2C10184513%2C10187546%2C10236938%2C10242931%2C10251872%2C10260657%2C10266242%2C10276670%2C10279081%2C10300338%2C10300454%2C10301078%2C10311511%2C10328296%2C10329430%2C10336462%2C10336473%2C10336987%2C10342315%2C10351429%2C10352297%2C10365307%2C10370756%2C668906%2C9960584%2C10344507%2C10364834%2C668905%2C10344506%2C668904%2C10344522%2C668903%2C10344537%2C668776%2C10344552%2C10307730%2C10345633%2C10351259%2C668907%2C9837813%2C10344534%2C668908%2C10344548%2C1859936%2C5315659%2C9153040%2C9259782%2C10234669%2C9101858%2C10139069%2C7142413%2C8504307%2C8612126%2C9751406%2C9758710%2C10049555%2C9416947%2C9470968%2C9797523%2C10036512%2C10068099%2C10102443%2C10105788%2C10196525%2C10289988&ab_client=a1%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&ssmix=a&device_type=PGAM10&device_brand=OPPO&language=zh&os_api=32&os_version=12&manifest_version_code=8620&resolution=1080*1920&dpi=480&update_version_code=86211&_rticket=1728537258848&sa_enable=0&dq_param=0&plugin_state=280419485511709&session_id=7648f3f6-34a8-40b0-871b-feef2e7ce106&host_abi=armeabi-v7a&tma_jssdk_version=2.8.0.14&rom_version=coloros__v417ir+release-keys&cdid=71199617-caa9-4030-9ea7-29ac881ce189'
        )
        return await self.handle_detail(data, url_template)

    async def xg_aweme_detail(self, data):
        url_template = (
            'https://ib.snssdk.com/video/app/article/full/15/1/{aweme_id}/0/0/0/?ac=wifi&channel=vivo_32_tr_x64&aid=32&app_name=video_article&version_code=110808&version_name=11.8.8&device_platform=android&os=android&ssmix=a&device_type=PGAM10&device_brand=OPPO&language=zh&os_api=32&os_version=12&manifest_version_code=788&resolution=1080*1920&dpi=480&update_version_code=11080807&_rticket=1745478959838&pad_adapter_type=0&package=com.ss.android.article.video&cdid_ts=1745478826081&is_android_pad=0&ipad_adapter_enable=0&device_platform_ext=phone&host_abi=arm64-v8a&tma_jssdk_version=2010000&rom_version=coloros__V417IR+release-keys&cdid=299e2686-2ec9-4df8-8d5c-43f56ecd8deb'
        )
        return await self.handle_detail(data, url_template)

    async def xg_aweme_detail_v2(self, data):
        url_template = (
            'https://ib.snssdk.com/video/app/article/information/v23/?group_id={aweme_id}&item_id={aweme_id}&aggr_type=2&context=1&hot_push=0&flags=64&from_category=pgc&article_page=1&disable_video_extensions_ad=0&ad_count=1&play_param=codec_type%3A7%2Ccdn_type%3A2%2Cenable_dash%3A1%2Cis_order_flow%3A-1%2Cis_hdr%3A1%2Cresolution%3A1080*1920&image_control=%7B%22avatar%22%3A%7B%22width%22%3A120%2C%22height%22%3A120%2C%22format%22%3A%22webp%22%7D%2C%22cover_image_large%22%3A%7B%22format%22%3A%22heic%22%7D%2C%22cover_image_middle%22%3A%7B%22format%22%3A%22heic%22%7D%7D&device_platform=android&os=android&ssmix=a&_rticket=1719382142115&cdid=d7779a41-9f72-4293-a55f-01fc54abe7dd&channel=vivo_32_tr_x64&aid=32&app_name=video_article&version_code=120500&version_name=12.5.0&manifest_version_code=850&update_version_code=12050006&ab_version=668856%2C9273984%2C9341568%2C9342000%2C3795189%2C3928650%2C4113875%2C4388054%2C4522571%2C4890005%2C5361616%2C5490178%2C6034694%2C6461462%2C6478709%2C6571797%2C6760626%2C6868069%2C7204589%2C7237725%2C7354844%2C7551466%2C7600619%2C7659314%2C7670553%2C7673025%2C7681478%2C7682666%2C7684446%2C8087081%2C8160328%2C8186512%2C8247505%2C8426870%2C8495268%2C8512477%2C8553218%2C8611793%2C8639938%2C8663350%2C8675077%2C8721367%2C8760182%2C8779948%2C8885972%2C8910511%2C8944448%2C8945471%2C8945517%2C8980675%2C8983679%2C8985781%2C9016791%2C9023658%2C9023670%2C9023693%2C9028094%2C9028101%2C9034363%2C9044861%2C9067502%2C9133021%2C9158364%2C9172702%2C9172964%2C9182348%2C9183639%2C9200775%2C9206408%2C9206929%2C9216069%2C9228821%2C9236942%2C9260772%2C9262164%2C9282281%2C9282990%2C9283006%2C9291727%2C9292375%2C9292489%2C9292540%2C9293770%2C9295447%2C9311414%2C9317190%2C9327573%2C9328924%2C9329064%2C9332996%2C9336569%2C9338659%2C9342316%2C9344219%2C9349043%2C9360760%2C9361205%2C9364453%2C9364475%2C9364939%2C9365265%2C9365476%2C9094555%2C668859%2C9273981%2C668858%2C9273942%2C668854%2C5370398%2C9249732%2C9273975%2C9277141%2C668853%2C9274002%2C668852%2C9273947%2C668855%2C9273955%2C668851%2C9273992%2C8916420%2C9126190%2C9191444%2C9276156%2C9295319%2C9346567%2C7142413%2C8504306%2C9181936%2C9227033%2C9288817%2C9347532&resolution=1080*1920&dpi=480&device_type=22021211RC&device_brand=Redmi&language=zh&os_api=32&os_version=12&ac=wifi&pad_adapter_type=0&package=com.ss.android.article.video&cdid_ts=1719373519496&is_android_pad=0&ipad_adapter_enable=0&device_platform_ext=phone&host_abi=arm64-v8a&tma_jssdk_version=2010000&rom_version=V417IR+release-keys&iid={install_id_str}&device_id={device_id_str}&klink_egdi=&openudid='
        )
        return await self.handle_detail(data, url_template)

    async def xg_user_detail(self, data):
        url_template = (
            'https://ib.snssdk.com/video/app/user/userhome/v8/?to_user_id={aweme_id}&enable_fav_history_tabs=0&has_favorite_folder=false&device_platform=android&os=android&ssmix=a&_rticket=1719382804296&cdid=d7779a41-9f72-4293-a55f-01fc54abe7dd&channel=vivo_32_tr_x64&aid=32&app_name=video_article&version_code=120500&version_name=12.5.0&manifest_version_code=850&update_version_code=12050006&ab_version=668856%2C9273984%2C9341568%2C9342000%2C3795189%2C3928650%2C4113875%2C4388054%2C4522571%2C4890005%2C5361616%2C5490178%2C6034694%2C6461462%2C6478709%2C6571797%2C6760626%2C6868069%2C7204589%2C7237725%2C7354844%2C7551466%2C7600619%2C7659314%2C7670553%2C7673025%2C7681478%2C7682666%2C7684446%2C8087081%2C8160328%2C8186512%2C8247505%2C8426870%2C8495268%2C8512477%2C8553218%2C8611793%2C8639938%2C8663350%2C8675077%2C8721367%2C8760182%2C8779948%2C8885972%2C8910511%2C8944448%2C8945471%2C8945517%2C8980675%2C8983679%2C8985781%2C9016791%2C9023658%2C9023670%2C9023693%2C9028094%2C9028101%2C9034363%2C9044861%2C9067502%2C9133021%2C9158364%2C9172702%2C9172964%2C9182348%2C9183639%2C9200775%2C9206408%2C9206929%2C9216069%2C9228821%2C9236942%2C9260772%2C9262164%2C9282281%2C9282990%2C9283006%2C9291727%2C9292375%2C9292489%2C9292540%2C9293770%2C9295447%2C9311414%2C9317190%2C9327573%2C9328924%2C9329064%2C9332996%2C9336569%2C9338659%2C9342316%2C9344219%2C9349043%2C9360760%2C9361205%2C9364453%2C9364475%2C9364939%2C9365265%2C9365476%2C9094555%2C668859%2C9273981%2C668858%2C9273942%2C668854%2C5370398%2C9249732%2C9273975%2C9277141%2C668853%2C9274002%2C668852%2C9273947%2C668855%2C9273955%2C668851%2C9273992%2C8916420%2C9126190%2C9191444%2C9276156%2C9295319%2C9346567%2C7142413%2C8504306%2C9181936%2C9227033%2C9288817%2C9347532&resolution=1080*1920&dpi=480&device_type=22021211RC&device_brand=Redmi&language=zh&os_api=32&os_version=12&ac=wifi&pad_adapter_type=0&package=com.ss.android.article.video&cdid_ts=1719373519496&is_android_pad=0&ipad_adapter_enable=0&device_platform_ext=phone&host_abi=arm64-v8a&tma_jssdk_version=2010000&rom_version=V417IR+release-keys&iid={install_id_str}&device_id={device_id_str}&klink_egdi='
        )
        return await self.handle_detail(data, url_template)

    async def xg_user_post(self, data):
        url_template = (
            'https://ib.snssdk.com/video/app/user/videolist_tab/v3/?play_param=codec_type%3A7%2Ccdn_type%3A2%2Cenable_dash%3A1%2Cis_order_flow%3A-1%2Cis_hdr%3A1%2Cresolution%3A1080*1920&orderby=publishtime&to_user_id={aweme_id}&isBackground=False&tab=video&count={count}&offset={offset}&max_behot_time={behot_time}&enable_publish_status=0&last_watch_gid=7361200528300330294&last_watch_query=false&scenes&device_platform=android&os=android&ssmix=a&_rticket=1719384276567&cdid=d7779a41-9f72-4293-a55f-01fc54abe7dd&channel=vivo_32_tr_x64&aid=32&app_name=video_article&version_code=120500&version_name=12.5.0&manifest_version_code=850&update_version_code=12050006&ab_version=668856%2C9273984%2C9341568%2C9342000%2C3795189%2C3928650%2C4113875%2C4388054%2C4522571%2C4890005%2C5361616%2C5490178%2C6034694%2C6461462%2C6478709%2C6571797%2C6760626%2C6868069%2C7204589%2C7237725%2C7354844%2C7551466%2C7600619%2C7659314%2C7670553%2C7673025%2C7681478%2C7682666%2C7684446%2C8087081%2C8160328%2C8186512%2C8247505%2C8426870%2C8495268%2C8512477%2C8553218%2C8611793%2C8639938%2C8663350%2C8675077%2C8721367%2C8760182%2C8779948%2C8885972%2C8910511%2C8944448%2C8945471%2C8945517%2C8980675%2C8983679%2C8985781%2C9016791%2C9023658%2C9023670%2C9023693%2C9028094%2C9028101%2C9034363%2C9044861%2C9067502%2C9133021%2C9158364%2C9172702%2C9172964%2C9182348%2C9183639%2C9200775%2C9206408%2C9206929%2C9216069%2C9228821%2C9236942%2C9260772%2C9262164%2C9282281%2C9282990%2C9283006%2C9291727%2C9292375%2C9292489%2C9292540%2C9293770%2C9295447%2C9311414%2C9317190%2C9327573%2C9328924%2C9329064%2C9332996%2C9336569%2C9338659%2C9342316%2C9344219%2C9349043%2C9360760%2C9361205%2C9364453%2C9364475%2C9364939%2C9365265%2C9365476%2C9094555%2C668859%2C9273981%2C668858%2C9273942%2C668854%2C5370398%2C9249732%2C9273975%2C9277141%2C668853%2C9274002%2C668852%2C9273947%2C668855%2C9273955%2C668851%2C9273992%2C8916420%2C9126190%2C9191444%2C9276156%2C9295319%2C9346567%2C7142413%2C8504306%2C9181936%2C9227033%2C9288817%2C9347532&resolution=1080*1920&dpi=480&device_type=22021211RC&device_brand=Redmi&language=zh&os_api=32&os_version=12&ac=wifi&pad_adapter_type=0&package=com.ss.android.article.video&cdid_ts=1719373519496&is_android_pad=0&ipad_adapter_enable=0&device_platform_ext=phone&host_abi=arm64-v8a&tma_jssdk_version=2010000&rom_version=V417IR+release-keys&iid={install_id_str}&device_id={device_id_str}&klink_egdi='
        )
        return await self.handle_detail(data, url_template)

    async def user_post(self, data):
        url = f"https://www.toutiao.com/api/pc/list/user/feed"
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        params = f"category={data.get('category', 'profile_all')}&token={data.get('sec_user_id', '')}&max_behot_time={data.get('max_behot_time', '')}&entrance_gid=&aid=24&app_name=toutiao_web&msToken="

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.toutiao.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ua,
            'Host': 'www.toutiao.com',
            'Connection': 'keep-alive'
        }
        params = await self.process_a_bogus(params, ua)
        url = f"{url}?{params}"
        response = await self.request.app.ctx.curl_client.http_get(url, headers=headers,
                                                                   proxy=await get_request_proxy(self.request))
        data = response.json()
        return json_success_response(data)

    async def article_information(self, data):
        url = f"https://lf5-article.toutiaostatic.com/article/full/125/0/{data.get('item_id')}/0/0/0/0/0/0f35e2858f6f23fab49cc74e768cf5/34/"
        headers = {
            "User-Agent": "com.ss.android.article.news/12000 (Linux; U; Android 12; zh_CN; 22021211RC; Build/V417IR;tt-ok/3.12.13.18)",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip",
            "x-vc-bdturing-sdk-version": "3.7.2.cn",
            "sdk-version": "2",
            "passport-sdk-version": "505107",
            "x-tt-request-tag": "n=0",
            "x-tt-store-region": "cn-ah",
            "x-tt-store-region-src": "did"
        }
        response = await self.request.app.ctx.curl_client.http_get(url, headers=headers,
                                                                   proxy=await get_request_proxy(self.request))
        data = response.json()
        return json_success_response(data)
