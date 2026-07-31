import json
import time
from asyncio import CancelledError
from typing import Dict, Any

from loguru import logger
from sanic import Request, HTTPResponse

from core import CustomException
from middleware.base import BaseMiddleware


class ResponseMiddleware(BaseMiddleware):
    async def before_request(self, request: Request) -> None:
        pass

    async def before_response(self, request: Request, response: HTTPResponse) -> None:
        """处理响应数据和记录日志"""
        elapsed_time = time.perf_counter() - request.ctx.start_time
        request_time = f"{elapsed_time:.5f}s"

        logger.info(f"请求接口 -- {request.path} -- 耗时 {request_time} -- {response.status}")

        # 处理自定义响应头
        if hasattr(request.ctx, 'response_headers'):
            response_headers = request.ctx.response_headers
            for key, value in response_headers.items():
                response.headers.update({key: value})
        if not "application/json" in response.content_type:
            return

        try:
            if request.name == "application.doc":
                return
            response_body = json.loads(response.body)
            response_data = await self._build_response_data(
                request=request,
                response_body=response_body,
                request_path=request.path,
                request_time=request_time
            )

            response.body = self._encode_response(response_data)

        except CancelledError:
            logger.info(f"请求被用户中断: {request.path}")
            return
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {request.path} - {str(e)}")
            raise CustomException(message=f"响应数据格式错误: {str(e)}")
        except KeyError as e:
            logger.warning(f"缺少必要字段: {request.path} - 缺少 {str(e)}")
            return
        except Exception as e:
            logger.error(f"响应处理异常: {request.path} - {str(e)}")
            raise CustomException(message=f"响应处理失败: {str(e)}")

    async def _build_response_data(self, request: Request, response_body: Dict[str, Any], request_path: str,
                                   request_time: str) -> Dict[str, Any]:
        """构建统一格式的响应数据"""
        try:
            proxy = request.ctx.request_proxy
        except CancelledError:
            logger.warning(f"构建响应数据时请求被用户中断: {request_path}")
            raise
        except:
            proxy = None
        
        # 构建基本响应数据结构
        response_data = {
            "code": response_body["code"],
            "path": request_path,
            "time": request_time,
            "msg": response_body["msg"],
            "proxy": proxy,
            **{k: v for k, v in response_body.items() if k not in ["code", "msg"]}
        }
        
        return response_data

    @staticmethod
    def _encode_response(data: Dict[str, Any]) -> bytes:
        """编码响应数据为bytes"""
        try:
            return json.dumps(
                data,
                ensure_ascii=False,
                separators=(",", ":"),
                indent=None
            ).encode("utf-8")
        except Exception as e:
            logger.error(f"响应数据编码失败: {str(e)}")
            return json.dumps({
                "code": 500,
                "msg": "响应数据处理失败",
                "data": None
            }).encode("utf-8")
