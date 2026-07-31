from __future__ import annotations

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.api_client import LocalApiClient
from app.secure_store import SettingsStore
from app.server_manager import ServerManager


release_data = root / "release" / "DouyinLeadSystem-Portable" / "data"
settings = SettingsStore(release_data / "settings.json")
order = settings.get_secret("order_number")
cookie = settings.get_secret("douyin_cookie")
manager = ServerManager(root / "server" / "APIServer_v5.3.1", root / "data" / "logs" / "cert-fix-live.log")
try:
    ok, message = manager.start(order, timeout=40)
    print({"server_ready": ok, "message": message, "login_saved": bool(cookie)})
    if not ok:
        raise RuntimeError(message)
    client = LocalApiClient(manager.base_url, "", 1.0, cookie)
    _result, videos = client.search_videos("智能工牌", 3)
    print({"videos": len(videos), "first_title": videos[0].get("title", "")[:80] if videos else ""})
finally:
    manager.stop()
