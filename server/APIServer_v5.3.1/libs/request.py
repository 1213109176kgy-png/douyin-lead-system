import json

from loguru import logger
from sanic import Request


async def get_request_data(request: Request) -> dict:
    """
    获取请求体
    :param request:
    :return:
    """
    result = {}
    headers = dict(request.headers)
    result.update(headers)

    url_params = {k: v[0] if len(v) == 1 else v for k, v in request.args.items()}
    result.update(url_params)
    if request.form:
        form_data = {k: v[0] if len(v) == 1 else v for k, v in request.form.items()}
        result.update(form_data)
    if "application/json" in request.content_type:
        try:
            if request.body:
                json_data = request.json
                if json_data:
                    result.update(json_data if isinstance(json_data, dict) else {"_json_body": json_data})
        except Exception as e:
            logger.warning(f"JSON解析失败: {str(e)}")
            result["_json_parse_error"] = str(e)
    if "text/plain" in request.content_type:
        request_data = json.loads(request.body)
        result.update(request_data)
    result.update({
        "_request_method": request.method,
        "_request_path": request.path,
        "_request_ip": request.ip,
    })
    return result


async def get_request_proxy(request: Request, proxy_type=None) -> str | None:
    """
    获取请求体中的代理
    :param request: 请求对象
    :return: 代理地址字符串或None
    """
    request_data = await get_request_data(request)
    proxy = request_data.get("proxy", None)
    if proxy_type == "overseas":
        sys_proxy = request.app.config.get("OVERSEAS_PROXY_URL",
                                           None)
    else:
        sys_proxy = request.app.config.get("CHINESE_PROXY_URL",
                                           None)

    if proxy == "" or not proxy:
        if sys_proxy == "":
            return None
        if sys_proxy == "redis":
            proxy_ip = await get_proxy_ip_from_cache(request)
            return proxy_ip
        return sys_proxy
    if str(proxy) == "False" or str(proxy) == "false" or str(proxy) == "null" or str(proxy) == "None":
        return None
    return proxy


async def get_proxy_ip_from_cache(request: Request):
    if hasattr(request.app.ctx, "redis_client"):
        client = request.app.ctx.redis_client
        random_key = await client.randomkey()
        if not random_key:
            logger.error("无法从 Redis 获取随机键")
            return None
        key_type = await client.type(random_key)
        key_str = random_key.decode()
        if key_type.decode() == 'string':
            value = await client.get(random_key)
            result = f"http://{key_str}:{value.decode()}"
            return result
        else:
            logger.warning(f"获取的 Redis 键 {key_str} 不是字符串类型")
            return None
    return None