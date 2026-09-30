from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote


root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")

from playwright.sync_api import sync_playwright

from app.api_client import LocalApiClient, parse_comments
from app.douyin_browser import (
    SEARCH_SCRIPT,
    cookie_records_from_header,
    edge_profile_dir,
    launch_persistent_browser,
    playwright_cookies_logged_in,
)
from app.paths import resolve_paths
from app.secure_store import SettingsStore
from app.server_manager import ServerManager


def main() -> int:
    paths = resolve_paths(root).ensure()
    settings = SettingsStore(paths.settings)
    cookie = settings.get_secret("douyin_cookie")
    if not cookie:
        print(json.dumps({"ok": False, "stage": "login", "error": "no_saved_login"}))
        return 2

    result = {"ok": False, "stage": "browser", "browser": "", "logged_in": False, "videos": 0, "comments": 0}
    rows: dict[str, dict] = {}
    with sync_playwright() as playwright:
        context, browser_name = launch_persistent_browser(playwright, edge_profile_dir(paths.data), print)
        result["browser"] = browser_name
        context.add_cookies(cookie_records_from_header(cookie))
        page = context.pages[0] if context.pages else context.new_page()
        keyword = "盲盒"
        page.goto(
            "https://www.douyin.com/search/" + quote(keyword) + "?type=video",
            wait_until="domcontentloaded",
            timeout=45_000,
        )
        time.sleep(5)
        payload = {}
        for round_number in range(6):
            try:
                payload = page.evaluate(SEARCH_SCRIPT) or {}
            except Exception as exc:
                if "execution context was destroyed" in str(exc).lower() and round_number < 5:
                    time.sleep(4)
                    continue
                raise
            for row in payload.get("rows") or []:
                aweme_id = str(row.get("aweme_id", ""))
                if aweme_id:
                    rows[aweme_id] = row
            if len(rows) >= 3:
                break
            page.mouse.wheel(0, 1100)
            time.sleep(3)
        result["logged_in"] = playwright_cookies_logged_in(context.cookies("https://www.douyin.com/"))
        result["videos"] = len(rows)
        result["search_page"] = "/search/" in page.url
        screenshot = paths.data / "screenshots" / "edge-live-search.png"
        screenshot.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot), full_page=False)
        result["screenshot"] = str(screenshot)
        context.close()

    if not rows:
        result["stage"] = "search"
        print(json.dumps(result, ensure_ascii=False))
        return 3

    manager = ServerManager(paths.server, paths.logs / "apiserver-e2e-smoke.log")
    try:
        ok, message = manager.start(cookie)
        if not ok:
            result.update(stage="server", error=message)
            print(json.dumps(result, ensure_ascii=False))
            return 4
        aweme_id = next(iter(rows))
        client = LocalApiClient(manager.base_url, "", 0.2, cookie)
        payload = client.post("/api/douyin/video_comment", {"aweme_id": aweme_id, "count": 10, "cursor": 0})
        comments = parse_comments(payload)
        result["comments"] = len(comments)
        result["comment_has_real_id"] = bool(comments and comments[0].get("comment_id"))
        result["profile_url_available"] = bool(comments and comments[0].get("profile_url"))
        result["stage"] = "complete"
        result["ok"] = bool(result["logged_in"] and result["videos"] and result["comments"])
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["ok"] else 5
    finally:
        manager.stop()


if __name__ == "__main__":
    raise SystemExit(main())
