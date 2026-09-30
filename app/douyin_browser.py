from __future__ import annotations

import json
import os
import random
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from PySide6.QtCore import QObject, QThread, Signal


AUTH_COOKIE_NAMES = {"sessionid", "sessionid_ss", "sid_guard"}
CHALLENGE_WORDS = ("验证码", "安全验证", "访问过于频繁", "操作频繁", "环境异常")
GATEWAY_WORDS = ("502 Bad Gateway", "503 Service Unavailable", "504 Gateway Timeout")


def cookie_header_from_playwright(cookies: list[dict]) -> str:
    pairs = {
        str(item.get("name", "")): str(item.get("value", ""))
        for item in cookies
        if "douyin.com" in str(item.get("domain", "")).lower()
        and item.get("name")
        and item.get("value")
    }
    return "; ".join(f"{name}={value}" for name, value in sorted(pairs.items()))


def cookie_records_from_header(header: str) -> list[dict]:
    records = []
    for part in (header or "").split(";"):
        if "=" not in part:
            continue
        name, value = part.strip().split("=", 1)
        if name and value:
            records.append({"name": name, "value": value, "domain": ".douyin.com", "path": "/"})
    return records


def playwright_cookies_logged_in(cookies: list[dict]) -> bool:
    values = {str(item.get("name", "")): str(item.get("value", "")) for item in cookies}
    return any(values.get(name) for name in AUTH_COOKIE_NAMES) or values.get(
        "passport_auth_status", ""
    ).lower() in {"1", "true", "success"}


def edge_profile_dir(data_dir: Path) -> Path:
    path = Path(data_dir) / "douyin-edge-profile"
    path.mkdir(parents=True, exist_ok=True)
    return path


def require_playwright():
    # The release bundles Chromium next to the Playwright Python package.
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("缺少浏览器运行组件，请重新安装或更新本程序") from exc
    return sync_playwright


def launch_persistent_browser(playwright, profile_dir: Path, status=None):
    """Prefer system Edge and fall back to the Chromium shipped with the app."""
    options = {
        "headless": False,
        "viewport": {"width": 1280, "height": 820},
        "locale": "zh-CN",
        # Playwright disables Chromium's sandbox by default. On Windows it is
        # unnecessary and exposes a warning banner that makes the session less
        # like an ordinary user browser.
        "ignore_default_args": ["--no-sandbox"],
    }
    try:
        context = playwright.chromium.launch_persistent_context(
            str(profile_dir), channel="msedge", **options
        )
        return context, "Microsoft Edge"
    except Exception as edge_error:
        if status:
            status("未检测到可用的 Microsoft Edge，正在切换到软件内置浏览器…")
        try:
            context = playwright.chromium.launch_persistent_context(str(profile_dir), **options)
            return context, "内置 Chromium"
        except Exception as bundled_error:
            raise RuntimeError(
                "系统 Edge 和软件内置 Chromium 均无法启动。"
                f" Edge：{str(edge_error)[:120]}；内置浏览器：{str(bundled_error)[:160]}"
            ) from bundled_error


def _parse_datetime(value) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def should_retry_destroyed_context(message: str, round_number: int, max_rounds: int = 6) -> bool:
    return "execution context was destroyed" in message.lower() and round_number < max_rounds


class SearchPolicy:
    """Conservative local pacing and circuit breaker for one Douyin account."""

    MIN_SEARCH_INTERVAL_SECONDS = 35
    ABNORMAL_COOLDOWN_MINUTES = 20
    GATEWAY_COOLDOWN_MINUTES = 5

    def __init__(self, data_dir: Path):
        self.path = Path(data_dir) / "douyin-search-policy.json"

    def _load(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return {}

    def _save(self, payload: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def seconds_until_allowed(self) -> tuple[int, str]:
        now = datetime.now()
        state = self._load()
        cooldown = _parse_datetime(state.get("cooldown_until"))
        if cooldown and cooldown > now:
            return max(1, int((cooldown - now).total_seconds())), "检测到上次搜索页面异常，正在保护账号"
        last = _parse_datetime(state.get("last_search_at"))
        if last:
            remaining = self.MIN_SEARCH_INTERVAL_SECONDS - int((now - last).total_seconds())
            if remaining > 0:
                return remaining, "距离上次搜索过近，正在排队"
        return 0, ""

    def record_started(self) -> None:
        state = self._load()
        state["last_search_at"] = datetime.now().isoformat(timespec="seconds")
        self._save(state)

    def record_success(self) -> None:
        state = self._load()
        state.pop("cooldown_until", None)
        state["last_success_at"] = datetime.now().isoformat(timespec="seconds")
        self._save(state)

    def record_abnormal(self) -> None:
        state = self._load()
        state["cooldown_until"] = (
            datetime.now() + timedelta(minutes=self.ABNORMAL_COOLDOWN_MINUTES)
        ).isoformat(timespec="seconds")
        self._save(state)

    def record_gateway_failure(self) -> None:
        state = self._load()
        state["cooldown_until"] = (
            datetime.now() + timedelta(minutes=self.GATEWAY_COOLDOWN_MINUTES)
        ).isoformat(timespec="seconds")
        self._save(state)


SEARCH_SCRIPT = r"""
() => {
  const body = document.body ? document.body.innerText : '';
  const seen = new Set();
  const rows = [];
  for (const a of document.querySelectorAll('a[href*="/video/"]')) {
    const href = a.href || '';
    const match = href.match(/\/video\/(\d+)/);
    if (!match || seen.has(match[1])) continue;
    seen.add(match[1]);
    // Walk upward only while the container still belongs to this one video.
    // Stopping at a multi-video ancestor prevents one grid item's longest text
    // from being assigned to every video on the page.
    let card = a;
    for (let i = 0; i < 7 && card.parentElement; i++) {
      const parent = card.parentElement;
      const videoIds = new Set();
      for (const link of parent.querySelectorAll('a[href*="/video/"]')) {
        const id = (link.href.match(/\/video\/(\d+)/) || [,''])[1];
        if (id) videoIds.add(id);
      }
      if (videoIds.size > 1) break;
      card = parent;
    }
    const attrs = [a.title, a.getAttribute('aria-label')];
    for (const el of card.querySelectorAll('[title],img[alt]')) {
      attrs.push(el.getAttribute('title'), el.getAttribute('alt'));
    }
    const texts = (attrs.join('\n') + '\n' + (a.innerText || '') + '\n' + (card.innerText || ''))
      .split('\n').map(x => x.trim()).filter(Boolean)
      .filter(x => !/^\d{1,2}:\d{2}$/.test(x))
      .filter(x => !/^\d+(\.\d+)?[万wW]?$/.test(x))
      .filter(x => !/^(点赞|评论|收藏|分享)$/.test(x))
      .sort((x, y) => y.length - x.length);
    const lines = (card.innerText || '').split('\n').map(x => x.trim()).filter(Boolean);
    const authorLine = lines.find(x => x.startsWith('@') && x.length > 1) || '';
    const metricText = lines.find(x => /^\d+(\.\d+)?(万|w|W)?$/.test(x)) || '';
    const parseCount = value => {
      const match = String(value).match(/^(\d+(?:\.\d+)?)(万|w|W)?$/);
      if (!match) return 0;
      return Math.round(Number(match[1]) * (match[2] ? 10000 : 1));
    };
    const user = card.querySelector && card.querySelector('a[href*="/user/"]');
    rows.push({
      aweme_id: match[1],
      title: texts.find(x => x.length > 3 && x.length < 180) || '',
      url: `https://www.douyin.com/video/${match[1]}`,
      author_uid: user ? ((user.href.match(/\/user\/([^/?]+)/) || [,''])[1]) : '',
      author_name: user ? (user.innerText || '').trim().replace(/^@/, '') : authorLine.replace(/^@/, ''),
      digg_count: parseCount(metricText), collect_count: 0, comment_count: 0
    });
  }
  return {body: body.slice(0, 12000), title: document.title, url: location.href, rows};
}
"""


class EdgeLoginWorker(QThread):
    status = Signal(str)
    logged_in = Signal(str)
    failed = Signal(str)

    def __init__(self, data_dir: Path, parent=None):
        super().__init__(parent)
        self.profile_dir = edge_profile_dir(data_dir)
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        try:
            sync_playwright = require_playwright()
            with sync_playwright() as playwright:
                context, browser_name = launch_persistent_browser(
                    playwright, self.profile_dir, self.status.emit
                )
                page = context.pages[0] if context.pages else context.new_page()
                page.goto("https://www.douyin.com/", wait_until="domcontentloaded", timeout=45_000)
                self.status.emit(f"请在弹出的{browser_name}窗口登录抖音；登录成功后程序会自动保存。")
                while not self._cancel.wait(1.0):
                    cookies = context.cookies("https://www.douyin.com/")
                    if playwright_cookies_logged_in(cookies):
                        header = cookie_header_from_playwright(cookies)
                        time.sleep(1)
                        break
                else:
                    header = ""
                context.close()
                if header and not self._cancel.is_set():
                    self.logged_in.emit(header)
        except Exception as exc:
            if not self._cancel.is_set():
                self.failed.emit(_friendly_browser_error(exc))


class _EdgeSearchWorker(QThread):
    status = Signal(str)
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, data_dir: Path, keyword: str, limit: int, cookie_header: str = "", parent=None):
        super().__init__(parent)
        self.profile_dir = edge_profile_dir(data_dir)
        self.keyword = keyword.strip()
        self.limit = max(1, int(limit))
        self.cookie_header = cookie_header
        self.policy = SearchPolicy(data_dir)
        self._cancel = threading.Event()

    def cancel(self):
        self._cancel.set()

    def _wait(self, seconds: float) -> bool:
        return self._cancel.wait(seconds)

    def run(self):
        try:
            remaining, reason = self.policy.seconds_until_allowed()
            while remaining > 0:
                if self._cancel.is_set(): return
                self.status.emit(f"{reason}，还需等待 {remaining} 秒…")
                step = min(5, remaining)
                if self._wait(step): return
                remaining -= step
            self.policy.record_started()
            sync_playwright = require_playwright()
            with sync_playwright() as playwright:
                self.status.emit("正在打开独立浏览器采集窗口…")
                context, browser_name = launch_persistent_browser(
                    playwright, self.profile_dir, self.status.emit
                )
                cookies = cookie_records_from_header(self.cookie_header)
                if cookies:
                    context.add_cookies(cookies)
                page = context.pages[0] if context.pages else context.new_page()
                url = "https://www.douyin.com/search/" + quote(self.keyword) + "?type=video"
                response = page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                self.status.emit(f"{browser_name}已打开搜索页，正在等待真实页面加载…")
                if self._wait(5): context.close(); return
                rows: dict[str, dict] = {}
                payload = {}
                gateway_seen = bool(response and response.status >= 500)
                gateway_retried = False
                for round_number in range(1, 7):
                    if self._cancel.is_set(): context.close(); return
                    try:
                        payload = page.evaluate(SEARCH_SCRIPT) or {}
                    except Exception as exc:
                        if should_retry_destroyed_context(str(exc), round_number):
                            self.status.emit("抖音页面正在完成跳转，等待稳定后继续读取…")
                            if self._wait(4): context.close(); return
                            continue
                        raise
                    title = str(payload.get("title", ""))
                    body = str(payload.get("body", ""))
                    if gateway_seen or any(word in title or word in body for word in GATEWAY_WORDS):
                        gateway_seen = True
                        if not gateway_retried:
                            gateway_retried = True
                            self.status.emit("抖音服务器返回网关错误，等待 15 秒后仅重载一次…")
                            if self._wait(15): context.close(); return
                            response = page.reload(wait_until="domcontentloaded", timeout=45_000)
                            gateway_seen = bool(response and response.status >= 500)
                            if self._wait(5): context.close(); return
                            continue
                        break
                    for row in payload.get("rows") or []:
                        aweme_id = str(row.get("aweme_id", ""))
                        if aweme_id:
                            row["title"] = str(row.get("title", "")).strip() or f"{self.keyword} · 抖音视频"
                            rows[aweme_id] = row
                    if len(rows) >= self.limit: break
                    self.status.emit(f"正在读取搜索结果（{round_number}/6），已找到 {len(rows)} 个视频…")
                    page.mouse.wheel(0, 900 + random.randint(0, 500))
                    if self._wait(2.5 + random.random() * 1.5): context.close(); return
                cookies = context.cookies("https://www.douyin.com/")
                body = str(payload.get("body", ""))
                current_url = str(payload.get("url", page.url))
                context.close()
                if not playwright_cookies_logged_in(cookies):
                    self.failed.emit(f"{browser_name}中的抖音登录已失效，请到系统设置重新登录")
                elif gateway_seen:
                    self.policy.record_gateway_failure()
                    self.failed.emit("抖音搜索服务器连续返回 502/503 网关错误；这不是登录问题，已停止重试并进入 5 分钟冷却")
                elif any(word in body for word in CHALLENGE_WORDS):
                    self.policy.record_abnormal()
                    self.failed.emit("抖音要求安全验证，已停止搜索并进入 20 分钟保护期；请在 Edge 中完成人工验证")
                elif rows:
                    self.policy.record_success(); self.finished.emit(list(rows.values())[: self.limit])
                elif "暂无" in body and self.keyword in body:
                    self.failed.emit(f"抖音搜索页正常返回，但关键词“{self.keyword}”当前没有视频结果")
                elif "/search/" not in current_url:
                    self.policy.record_abnormal()
                    self.failed.emit("抖音搜索页发生跳转，可能需要重新登录或人工验证；已停止自动重试")
                else:
                    self.policy.record_abnormal()
                    self.failed.emit("抖音搜索页已加载但无法识别视频列表，可能是页面结构变化或临时限制；已进入 20 分钟保护期")
        except Exception as exc:
            self.failed.emit(_friendly_browser_error(exc))


def _friendly_browser_error(exc: Exception) -> str:
    text = str(exc)
    lower = text.lower()
    if "系统 edge 和软件内置 chromium 均无法启动" in lower:
        return text[:500]
    if "user data directory is already in use" in lower:
        return "抖音专用浏览器会话正在被占用，请关闭弹出的采集窗口后重试"
    if "timeout" in lower:
        return "浏览器打开抖音页面超时，请检查网络后再试"
    return f"浏览器运行失败：{text[:300]}"


class DouyinBrowserSearch(QObject):
    status = Signal(str)
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, data_dir: Path, cookie_header: str = "", parent=None):
        super().__init__(parent)
        self.data_dir = Path(data_dir)
        self.cookie_header = cookie_header
        self.worker: _EdgeSearchWorker | None = None

    def start(self, keyword: str, limit: int):
        if self.worker and self.worker.isRunning():
            self.failed.emit("已有搜索任务正在运行，请等待当前任务结束")
            return
        self.worker = _EdgeSearchWorker(self.data_dir, keyword, limit, self.cookie_header, self)
        self.worker.status.connect(self.status)
        self.worker.finished.connect(self.finished)
        self.worker.failed.connect(self.failed)
        self.worker.start()

    def cancel(self):
        if self.worker and self.worker.isRunning(): self.worker.cancel()
