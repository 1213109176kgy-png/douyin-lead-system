from loguru import logger
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound, ServerError, MethodNotAllowed
from asyncio import CancelledError


class CustomException(Exception):
    """自定义异常基类"""

    def __init__(self, message="参数错误", status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class UnauthorizedError(CustomException):
    """未授权异常"""

    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)


class ProxyError(CustomException):
    """代理异常"""

    def __init__(self, message="代理异常"):
        super().__init__(message, status_code=417)


def setup_exception_handlers(app: Sanic):
    """
    设置自定义异常处理器
    """

    @app.exception(CancelledError)
    async def handle_cancelled_error(request, exception):
        """处理请求取消异常"""
        logger.warning(f"请求被用户中断: {request.path}")
        return json({
            "code": 499,  # 使用nginx的客户端关闭请求状态码
            "data": None,
            "msg": "请求被客户端中断"
        }, status=499)

    @app.exception(CustomException)
    async def handle_custom_exception(request, exception: CustomException):
        """处理自定义异常"""
        if getattr(app.config, "DEBUG", True):
            logger.exception(exception)
        return json({
            "code": exception.status_code,
            "data": None,
            "msg": exception.message
        }, status=exception.status_code)

    @app.exception(NotFound)
    async def handle_not_found(request, exception):
        """处理 404 异常"""
        logger.warning(f"请求地址非法")
        return json({
            "code": 404,
            "data": None,
            "msg": "请求地址非法"
        }, status=404)

    @app.exception(MethodNotAllowed)
    async def handle_method_not_allowed(request, exception):
        """处理 405 异常"""
        logger.warning(f"不允许的请求方式")

        return json({
            "code": 405,
            "data": None,
            "msg": "不允许的请求方式"
        }, status=405)

    @app.exception(Exception)
    async def handle_generic_exception(request, exception):
        """处理所有未捕获的异常"""
        logger.error(f"服务器错误: {exception}")
        return json({
            "code": 500,
            "msg": f"服务器错误: {exception}",
            "data": None
        }, status=500)
