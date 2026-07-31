import re
import secrets
from urllib.parse import urlparse, quote

from sanic import Request

from core import CustomException


async def extract_url(text: str) -> str:
    url_pattern = r'https?://[^\s/$.?#].[^\s]*'
    urls = re.findall(url_pattern, text)
    if urls:
        return urls[0]
    raise CustomException(message="share_text中提取url失败")

async def generate_random_string(length=64) -> str:
    """
    :param length: 生成字符串的位数
    :return:
    """
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_string = ''.join(secrets.choice(charset) for _ in range(length))
    return random_string


async def generate_random_string_alph(length=32, custom_alphabet="1234567890abcde") -> str:
    """
    生成指定位数并随机某些字符的字符串
    """
    return ''.join(secrets.choice(custom_alphabet) for _ in range(length))

async def get_domain_from_url(url):
    """
    从url字符串中提取出domain
    :param url:
    :return:
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def splitParams(url):
    params = url.split('?')[1]
    return params


def quote_keyword(keyword):
    keyword_list = keyword.split()
    encoded = "+".join(quote(word) for word in keyword_list)
    return encoded