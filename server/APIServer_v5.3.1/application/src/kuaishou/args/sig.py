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
@Project ：MoreAPI_Manage
@File    ：client.py
@IDE     ：PyCharm
@Author  ：
@Date    ：2024/11/15 9:49
@WebSite ：
'''
import string
import random
import hashlib
from urllib.parse import unquote, urlparse

from application import config


async def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


async def str_to_map(str_):
    return {i.split("=")[0]: i.split("=")[-1] for i in str_.split("&")}


async def map_to_str(map_):
    return "&".join([f"{i}={map_[i]}" for i in map_])


async def get_data_dict(request_data):
    request_data_dict = await str_to_map(request_data)
    if "sig" in request_data_dict:
        del request_data_dict["sig"]
    if "__NS_sig3" in request_data_dict:
        del request_data_dict["__NS_sig3"]
    if "__NStokensig" in request_data_dict:
        del request_data_dict["__NStokensig"]
    return request_data_dict


async def get_sig(url, request_data, salt="382700b563f4"):
    params_dict = await str_to_map(url.split("?")[-1])
    request_data_dict = await get_data_dict(request_data)
    params_dict.update(request_data_dict)
    temp_str = ""
    for key in sorted(params_dict):
        temp_str += key + "=" + unquote(params_dict[key])
    temp_str += salt
    return hashlib.md5(temp_str.encode()).hexdigest()


async def get_ns_token_sig(sig, token_client_salt="83e321352115762c7c3af1b490a72ee6"):
    return hashlib.sha256((sig + token_client_salt).encode()).hexdigest()


async def get_ks_sig3(http_client, base_url, sig):
    """
    此处是快手 app 端sig3签名  可单独购买算法服务搭建  https://www.wouldmissyou.com/2024/01/17/301/
    :param base_url:  请求url
    :param sig: sig值
    :return: 计算好的sig3
    """
    url = f"http://{getattr(config.BaseConfig, 'KS_SIGN_ORIGIN', '124.221.128.86:5516')}/api/ksh_10_5_40/sig3?url={base_url + sig}"
    response = await http_client.http_post(url=url, proxy=None)
    sig3 = response.text
    return sig3


async def get_payload(http_client, url, payload):
    sig = await get_sig(url, payload)
    request_data_dict = await get_data_dict(payload)
    request_data_dict["sig"] = sig
    url_pre = urlparse(url).path
    sig3 = await get_ks_sig3(http_client, url_pre, sig)
    request_data_dict["__NS_sig3"] = sig3
    request_data_dict["__NStokensig"] = await get_ns_token_sig(sig)
    change_payload = await map_to_str(request_data_dict)
    return change_payload
