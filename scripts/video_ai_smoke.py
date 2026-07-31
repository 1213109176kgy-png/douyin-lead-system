from __future__ import annotations

import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from app.api_client import LocalApiClient
from app.secure_store import SettingsStore
from app.server_manager import ServerManager
from app.video_ai import download_media, find_media_url, transcribe_local


settings = SettingsStore(root / "release" / "DouyinLeadSystem-Portable" / "data" / "settings.json")
manager = ServerManager(root / "server" / "APIServer_v5.3.1", root / "data" / "logs" / "video-ai-smoke.log")
try:
    ok, message = manager.start(settings.get_secret("order_number"), timeout=40)
    print({"server_ready": ok, "message": message})
    client = LocalApiClient(manager.base_url, "", 1.0, settings.get_secret("douyin_cookie"))
    _, videos = client.search_videos("智能工牌", 1)
    video = videos[0]
    detail = client.video_detail(video["aweme_id"])
    media_url = find_media_url(detail)
    print({"aweme_id": video["aweme_id"], "media_url_found": bool(media_url)})
    if not media_url:
        raise RuntimeError("media URL not found")
    with tempfile.TemporaryDirectory(prefix="douyin-video-ai-test-") as temp:
        path = download_media(media_url, Path(temp) / "video.mp4", settings.get_secret("douyin_cookie"))
        print({"download_mb": round(path.stat().st_size / 1024 / 1024, 2)})
        transcript = transcribe_local(path, root / "data" / "models", lambda text: print({"progress": text}))
        print({"transcript_chars": len(transcript), "preview": transcript[:200]})
finally:
    manager.stop()
