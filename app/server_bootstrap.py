from __future__ import annotations

import os
import sys
from pathlib import Path


def run_server(server_root: str | Path):
    root = Path(server_root).resolve()
    sys.path.insert(0, str(root))
    from application.config import BaseConfig

    BaseConfig.MOREAPI_ORDER_NUM = os.environ.get("MOREAPI_ORDER_NUM", "")
    BaseConfig.API_PWD = ""
    BaseConfig.CHINESE_PROXY_URL = ""
    BaseConfig.AUTO_RELOAD = False
    BaseConfig.DEBUG = False
    from application import create_app

    app = create_app()
    app.run(host="127.0.0.1", port=8001, auto_reload=False, access_log=False, single_process=True)
