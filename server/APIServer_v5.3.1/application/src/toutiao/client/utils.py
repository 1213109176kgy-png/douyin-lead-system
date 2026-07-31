#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：MoreAPI_Manager 
@File    ：utils.py
@IDE     ：PyCharm 

@Date    ：2025/3/14 16:20 
'''
import random

import aiofiles
import execjs


def get_ms_token(randomlength=107):
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789='
    return ''.join(random.choice(base_str) for _ in range(randomlength))

async def read_js_file(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        js_code = await file.read()
    return js_code


async def process_data_in_js(data):
    js_code = await read_js_file('application/src/toutiao/args/new_ab.js')
    context = execjs.compile(js_code)

    # 调用JS方法
    result = context.call('main', data)
    return result
