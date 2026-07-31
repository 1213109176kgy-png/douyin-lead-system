from sanic import Request, HTTPResponse

from middleware.base import BaseMiddleware


class CORSMiddleware(BaseMiddleware):
    """跨域中间件"""

    async def before_request(self, request: Request) -> None:
        pass

    async def before_response(self, request: Request, response: HTTPResponse) -> None:
        # 允许所有来源的跨域请求
        response.headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        })

        if request.method == "OPTIONS":
            response.status = 204
            return response 