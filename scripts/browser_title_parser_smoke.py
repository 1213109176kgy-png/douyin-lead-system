from __future__ import annotations

import os
import sys
from pathlib import Path


root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")

from playwright.sync_api import sync_playwright

from app.douyin_browser import SEARCH_SCRIPT


HTML = """
<div class="video-grid">
  <div class="video-card"><a href="https://www.douyin.com/video/10001"><img alt="第一个视频的真实标题"></a><a href="/user/a">作者甲</a></div>
  <div class="video-card"><a href="https://www.douyin.com/video/10002"><img alt="第二个视频完全不同的标题"></a><a href="/user/b">作者乙</a></div>
</div>
"""


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(HTML)
    rows = page.evaluate(SEARCH_SCRIPT)["rows"]
    browser.close()

assert [row["aweme_id"] for row in rows] == ["10001", "10002"]
assert [row["title"] for row in rows] == ["第一个视频的真实标题", "第二个视频完全不同的标题"]
print("title parser ok: 2 distinct video cards -> 2 distinct titles")
