import time

from sanic import Request, HTTPResponse

from libs import get_request_data
from middleware.base import BaseMiddleware
from core.exceptions import UnauthorizedError


class ClientMiddleware(BaseMiddleware):

    async def before_request(self, request: Request) -> None:
        request.ctx.request_data = await get_request_data(request)
        request.ctx.start_time = time.perf_counter()
        api_pwd = request.app.config.get('API_PWD')
        pwd_name = getattr(request.app.config, 'PWD_NAME', 'pwd') if getattr(request.app.config, 'PWD_NAME', 'pwd') not in (None, '') else 'pwd'
        if request.app.config.API_DOC_PATH in request.path or "/swagger/openapi" in request.path:
            return
        if api_pwd and api_pwd.strip():
            request_data = request.ctx.request_data
            request_pwd = request_data.get(pwd_name)
            if not request_pwd or request_pwd != api_pwd:
                raise UnauthorizedError("API密码不正确或未提供")

    async def before_response(self, request: Request, response: HTTPResponse) -> None:
        pass