from sanic import response


def json_response(code=200, data=None, message="success"):
    """
    通用json响应方法
    :param code: 响应码
    :param body: 响应主体
    :param data: 响应数据
    :param message: 响应信息
    :return: JSON
    """
    result = {
        "code": code,
        "msg": message,
        "data": data if data is not None else None
    }
    return response.json(result, content_type="application/json", status=code)


def json_success_response(data=None, code=200, message="success"):
    """
    通用  响应内容正确
    """
    return json_response(data=data, message=message, code=code)


def json_fail_response(code=400, data=None, message=None):
    """
    通用  响应内容错误
    """
    message = message if message is not None else "fail"

    return json_response(code=code, data=data, message=message)