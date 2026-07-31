#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：utils.py
@IDE     ：PyCharm 

@Date    ：2025/4/14 10:03 
'''
import base64
import binascii
import hashlib
import json
import random
import re
import string
import time
from io import BytesIO

import qrcode
from loguru import logger
from core import CustomException


async def extract_id(share_text: str, pattern: str):
    try:
        match = re.search(pattern, share_text)
        if not match:
            logger.warning(f"未能在分享文本中匹配到ID: {share_text}, 使用模式: {pattern}")
            return None
            
        if "/profile/" in share_text:
            return match.group(1), match.group(2)
            
        try:
            note_id = match.group(2)
            xsec_token = match.group(3)
        except IndexError:
            note_id = match.group(1)
            xsec_token = ""
            
        return note_id, xsec_token if note_id else ""
    except Exception as e:
        logger.error(f"提取ID失败: {str(e)}")
        raise CustomException(message=f"从分享链接提取ID失败: {str(e)}")

def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def get_search_id():
    e = int(time.time() * 1000) << 64
    t = int(random.uniform(0, 2147483646))
    return base36encode((e + t))


def get_a1_and_web_id():
    def random_str(length):
        alphabet = string.ascii_letters + string.digits
        return ''.join(random.choice(alphabet) for _ in range(length))

    try:
        d = hex(int(time.time() * 1000))[2:] + random_str(30) + "5" + "0" + "000"
        g = (d + str(binascii.crc32(str(d).encode('utf-8'))))[:52]
        return g, hashlib.md5(g.encode('utf-8')).hexdigest()
    except Exception as e:
        logger.error(f"生成a1和web_id失败: {str(e)}")
        timestamp = hex(int(time.time() * 1000))[2:]
        default_a1 = timestamp + "a" * 30 + "50000"
        default_webid = hashlib.md5(default_a1.encode('utf-8')).hexdigest()
        return default_a1, default_webid

async def get_secpoisonid():
    def generate_random_bytes():
        random_bytes = [0] * 16
        for i in range(16):
            if i % 4 == 0:
                random_value = random.randint(0, 0xFFFFFFFF)
            random_bytes[i] = (random_value >> ((i % 4) * 8)) & 0xFF
        return random_bytes

    def format_uuid(bytes):
        hex_values = [f"{i:02x}" for i in range(256)]

        uuid = (
                hex_values[bytes[0]] + hex_values[bytes[1]] + hex_values[bytes[2]] + hex_values[bytes[3]] + '-' +
                hex_values[bytes[4]] + hex_values[bytes[5]] + '-' +
                hex_values[bytes[6] | 0x40] + hex_values[bytes[7]] + '-' +
                hex_values[bytes[8] | 0x80] + hex_values[bytes[9]] + '-' +
                hex_values[bytes[10]] + hex_values[bytes[11]] + hex_values[bytes[12]] + hex_values[bytes[13]] +
                hex_values[bytes[14]] + hex_values[bytes[15]]
        ).lower()

        return uuid

    def generate_sec_poison_id():
        random_bytes = generate_random_bytes()
        return format_uuid(random_bytes)

    try:
        return generate_sec_poison_id()
    except Exception as e:
        logger.error(f"生成sec_poison_id失败: {str(e)}")
        return "00000000-0000-4000-8000-000000000000"


def camel_to_underscore(key):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()


def transform_json_keys(json_data):
    try:
        data_dict = json.loads(json_data)
        dict_new = {}
        for key, value in data_dict.items():
            new_key = camel_to_underscore(key)
            if not value:
                dict_new[new_key] = value
            elif isinstance(value, dict):
                dict_new[new_key] = transform_json_keys(json.dumps(value))
            elif isinstance(value, list):
                dict_new[new_key] = [
                    transform_json_keys(json.dumps(item))
                    if (item and isinstance(item, dict))
                    else item
                    for item in value
                ]
            else:
                dict_new[new_key] = value
        return dict_new
    except Exception as e:
        logger.error(f"转换JSON键名失败: {str(e)}")
        # 返回原始数据，避免处理中断
        try:
            return json.loads(json_data)
        except:
            return {}


async def parse_note_detail(text:str):
    try:
        initial_state_match = re.findall(r"window.__INITIAL_STATE__=({.*})</script>", text)
        if not initial_state_match:
            logger.warning("未找到匹配的笔记数据结构 __INITIAL_STATE__")
            return None
            
        data_json = initial_state_match[0].replace("undefined", '""')
        
        if text == "{}" or data_json == "{}":
            logger.warning("笔记数据为空")
            return None
        note_dict = transform_json_keys(data_json)
        pattern = r'[a-zA-Z0-9]{18,24}'
        if "note" not in note_dict or "note_detail_map" not in note_dict["note"]:
            logger.warning("笔记数据结构不完整")
            return None
        for note_id in note_dict["note"]["note_detail_map"]:
            if re.match(pattern, note_id):
                note_data = note_dict["note"]["note_detail_map"][note_id].get('note')
                if note_data:
                    return note_data
                    
        logger.warning("在笔记详情中未找到符合格式的笔记ID")
        return None
    except Exception as e:
        logger.error(f"解析笔记详情失败: {str(e)}")
        return None


async def parse_note_detail_v3(text:str):
    """
    解析移动端笔记详情页面数据
    
    Args:
        text: 页面HTML文本

    Returns:
        笔记详情数据
    """
    try:
        # 提取服务器状态数据
        setup_state_match = re.findall(r"window.__SETUP_SERVER_STATE__=({.*})</script>", text)
        if not setup_state_match:
            logger.warning("未找到匹配的笔记数据结构 __SETUP_SERVER_STATE__")
            return None
            
        data_json = setup_state_match[0].replace("undefined", '""')
        
        if text == "{}" or data_json == "{}":
            logger.warning("笔记数据为空")
            return None
            
        # 解析JSON数据
        result = json.loads(data_json)
        result = result.get("LAUNCHER_SSR_STORE_PAGE_DATA")

        if result:
            # 转换键名格式
            note_dict = transform_json_keys(json.dumps(result))
            return note_dict
        else:
            logger.warning("未找到LAUNCHER_SSR_STORE_PAGE_DATA字段")
            return None
    except Exception as e:
        logger.error(f"解析笔记详情v3失败: {str(e)}")
        return None


async def parse_user_detail(text:str):
    try:
        initial_state_match = re.findall(r"window.__INITIAL_STATE__=({.*})</script>", text)
        if not initial_state_match:
            logger.warning("未找到匹配的用户数据结构 __INITIAL_STATE__")
            return None

        data_json = initial_state_match[0].replace("undefined", '123')
        if text == "{}" or data_json == "{}":
            logger.warning("用户数据为空")
            return None
        data_json.replace('""""', '"1"')
        # 转换键名格式
        user_dict = transform_json_keys(data_json)
        if "user" not in user_dict:
            logger.warning("用户数据结构不完整")
            return None
        return user_dict['user']['user_page_data']
    except Exception as e:
        logger.error(f"解析用户详情失败: {str(e)}")
        return None





async def qr_to_base64(text:str):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    except Exception as e:
        logger.error(e)
        raise CustomException(message="转换二维码失败")

def remove_web_session(cookie_string, reserve_session=True):
    if reserve_session:
        return re.sub(r'(web_session=)[^;]+', r'\1', cookie_string)
    return re.sub(r'web_session=[^;]+;?', '', cookie_string)



def extract_cookies(cookie_str):
    """
    从原始 Cookie 字符串提取并格式化为 `xxx=xxx; xxx=xxx;` 的形式

    Args:
        cookie_str (str): 原始 Cookie 字符串

    Returns:
        str: 格式化后的 Cookie 字符串，如 `key1=value1; key2=value2;`
    """
    cookies = []
    # 按逗号分割每个 Cookie（去除空格）
    cookie_list = [cookie.strip() for cookie in cookie_str.split(",")]

    for cookie in cookie_list:
        # 取第一个分号前的键值对
        key_value = cookie.split(";")[0].strip()
        if "=" in key_value:
            cookies.append(key_value)

    # 用分号和空格连接所有 Cookie
    return "; ".join(cookies) + ";"