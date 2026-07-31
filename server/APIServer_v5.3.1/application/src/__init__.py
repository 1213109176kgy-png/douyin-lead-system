import importlib
import os
import sys
import traceback
from typing import Dict, Tuple, List

from loguru import logger
from sanic import Blueprint, Sanic

base_path = "application/src"
base_import = "application.src"


def list_directories() -> List[str]:
    try:
        path = base_path
        return [entry.name for entry in os.scandir(path) if entry.is_dir() and entry.name != '__pycache__']
    except Exception as e:
        logger.error(f"获取目录列表失败: {str(e)}")
        return []


def check_sys_path():
    logger.debug(f"Python系统路径: {sys.path}")
    logger.debug(f"当前工作目录: {os.getcwd()}")


def import_routers(base_path: str, base_import: str) -> Dict[str, Blueprint]:
    routers = {}
    directories = list_directories()
    logger.info(f"发现应用目录: {', '.join(directories)}")
    
    check_sys_path()

    for directory in directories:
        module_name = f"{base_import}.{directory}"
        variable_name = f"{directory.upper()}_ROUTER"
        try:
            init_path = os.path.join(base_path, directory, "__init__.py")
            if not os.path.exists(init_path):
                logger.warning(f"应用 {directory} 中的 __init__.py 文件不存在，路径: {init_path}")
                continue
                
            # logger.debug(f"正在尝试导入模块: {module_name}")

            module = importlib.import_module(module_name)
            
            if hasattr(module, variable_name):
                router = getattr(module, variable_name)
                routers[variable_name] = router
                logger.success(f"成功导入应用 {directory} 的路由")
            else:
                all_attrs = dir(module)
                router_like_vars = [attr for attr in all_attrs if attr.endswith('_ROUTER')]
                logger.warning(f"应用 {directory} 中未定义 {variable_name} 变量，可用的类似路由变量: {router_like_vars}")
        except ModuleNotFoundError as e:
            logger.error(f"应用 {directory} 模块导入错误: {str(e)}")
            try:
                dir_files = os.listdir(os.path.join(base_path, directory))
                logger.debug(f"应用 {directory} 中的文件: {dir_files}")
            except Exception:
                pass
            logger.debug(f"导入错误详情: {traceback.format_exc()}")
        except ImportError as e:
            logger.error(f"应用 {directory} 导入依赖错误: {str(e)}")
            logger.debug(f"导入错误详情: {traceback.format_exc()}")
            if "circular import" in str(e).lower():
                logger.warning(f"应用 {directory} 可能存在循环导入问题")
        except AttributeError as e:
            logger.error(f"应用 {directory} 属性错误: {str(e)}")
            logger.debug(f"错误详情: {traceback.format_exc()}")
        except Exception as e:
            logger.error(f"加载应用 {directory} 时发生未知错误: {type(e).__name__}: {str(e)}")
            logger.debug(f"错误详情: {traceback.format_exc()}")

    if not routers:
        logger.warning("未找到任何有效的路由蓝图!")
    else:
        logger.info(f"成功导入的应用: {', '.join(routers.keys())}")

    return routers


routers = import_routers(base_path, base_import)
APP_BLUE_TUPLE: Tuple[Blueprint, ...] = tuple(routers.values())


def register_blueprint(app: Sanic) -> None:
    api_base_path = app.config.get('API_BASIC_PATH', 'api')
    logger.info(f"API基础路径: /{api_base_path}/")

    if not APP_BLUE_TUPLE:
        logger.warning("没有可注册的蓝图，API功能将不可用")
        return

    for blueprint in APP_BLUE_TUPLE:
        try:
            url_prefix = f"/{api_base_path}/{blueprint.url_prefix}/"

            app.blueprint(blueprint, url_prefix=url_prefix)

            routes_count = len(blueprint.routes)
            logger.success(f"应用 {blueprint.name} 注册成功，包含 {routes_count} 个路由，前缀: {url_prefix}")
        except Exception as e:
            logger.error(f"注册应用 {blueprint.name} 失败: {str(e)}")
    logger.info(f"共注册 {len(APP_BLUE_TUPLE)} 个应用模块")
    return None
