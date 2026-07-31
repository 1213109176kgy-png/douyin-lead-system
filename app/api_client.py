from __future__ import annotations

import json
import time
import urllib.error
import urllib.request


def first(node: dict, keys: tuple[str, ...], default=""):
    for key in keys:
        value = node.get(key)
        if value not in (None, "", []):
            return value
    return default


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from walk(child)
    elif isinstance(value, list):
        for child in value: yield from walk(child)


def parse_videos(payload) -> list[dict]:
    found, seen = [], set()
    for node in walk(payload):
        aweme_id = str(first(node, ("aweme_id", "item_id"), ""))
        if not aweme_id or aweme_id in seen: continue
        author = node.get("author") if isinstance(node.get("author"), dict) else {}
        statistics = node.get("statistics") if isinstance(node.get("statistics"), dict) else {}
        found.append({"aweme_id": aweme_id, "title": str(first(node, ("desc", "title", "caption"), "")), "url": str(first(node, ("share_url", "url"), f"https://www.douyin.com/video/{aweme_id}")), "author_uid": str(first(author, ("sec_uid", "sec_user_id", "uid"), "")), "author_name": str(first(author, ("nickname", "name"), "")), "digg_count": int(first(statistics, ("digg_count", "like_count"), 0) or 0), "collect_count": int(first(statistics, ("collect_count", "favorite_count"), 0) or 0), "comment_count": int(first(statistics, ("comment_count",), 0) or 0)})
        seen.add(aweme_id)
    return found


def parse_comments(payload) -> list[dict]:
    found, seen = [], set()
    for node in walk(payload):
        text = first(node, ("text", "comment_text", "content"), "")
        user = first(node, ("user", "author", "comment_user"), {})
        if not isinstance(text, str) or not text.strip() or not isinstance(user, dict): continue
        cid = str(first(node, ("cid", "comment_id"), "")); uid = str(first(user, ("sec_uid", "sec_user_id", "uid", "user_id"), "")); nickname = str(first(user, ("nickname", "name", "display_name"), ""))
        key = cid or f"{uid}:{text.strip()}"
        if key in seen or not (uid or nickname): continue
        found.append({"comment_id": cid, "text": text.strip(), "user_id": uid, "nickname": nickname, "likes": int(first(node, ("digg_count", "like_count"), 0) or 0), "created_at": str(first(node, ("create_time", "timestamp"), "")), "profile_url": str(first(user, ("share_url", "profile_url"), f"https://www.douyin.com/user/{uid}" if uid else ""))})
        seen.add(key)
    return found


def page_info(payload) -> tuple[bool, str]:
    for node in walk(payload):
        if "has_more" in node or "hasMore" in node:
            return bool(first(node, ("has_more", "hasMore"), False)), str(first(node, ("next_cursor", "cursor", "offset"), ""))
    return False, ""


class LocalApiClient:
    def __init__(self, base_url="http://127.0.0.1:8001", password="", delay=1.2, cookie=""):
        self.base_url = base_url.rstrip("/"); self.password = password; self.delay = max(0.8, float(delay)); self.cookie = cookie.strip(); self.last_request = 0.0

    def post(self, endpoint: str, payload: dict, retries=3):
        if self.password: payload = {**payload, "pwd": self.password}
        wait = self.delay - (time.monotonic() - self.last_request)
        if wait > 0: time.sleep(wait)
        request = urllib.request.Request(self.base_url + endpoint, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), method="POST", headers={"Content-Type": "application/json;charset=utf-8"})
        # MoreAPI can accept the first search request while its comment clients are
        # still warming up. During that short window it returns HTTP 401 with
        # "MoreAPI未准备完毕"; a few seconds later the exact same request succeeds.
        # Give only this startup status a longer retry window. Persistent 401s
        # still surface as an error instead of being hidden indefinitely.
        max_attempts = max(retries, 5)
        for attempt in range(max_attempts):
            self.last_request = time.monotonic()
            try:
                with urllib.request.urlopen(request, timeout=40) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                retryable = exc.code in {401, 408, 425, 429}
                attempt_limit = max_attempts if exc.code == 401 else retries
                if not retryable:
                    raise RuntimeError(f"本地接口错误 HTTP {exc.code}") from exc
                if attempt >= attempt_limit - 1:
                    hint = "，上游请求超时，请稍后重试" if exc.code == 408 else ""
                    if exc.code == 401:
                        hint = "，本地服务初始化超时，请关闭软件后重新打开"
                    raise RuntimeError(f"本地接口错误 HTTP {exc.code}{hint}") from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt >= retries - 1:
                    raise RuntimeError(f"本地接口请求失败：{exc}") from exc
            time.sleep(min(2 ** attempt, 4))
        raise RuntimeError("本地接口请求失败")

    def search_videos(self, keyword: str, count: int):
        payload = {"keyword": keyword, "count": str(min(count, 18)), "offset": "0", "publish_time": "0", "filter_duration": "0", "sort_type": "0"}
        if self.cookie:
            payload["cookie"] = self.cookie
        messages = []
        for endpoint in ("/api/douyin/search_video", "/api/douyin/search_video_v3", "/api/douyin/search_video_v2"):
            result = self.post(endpoint, payload)
            videos = parse_videos(result)
            if videos:
                return result, videos
            data = result.get("data", {}) if isinstance(result, dict) else {}
            if isinstance(data, dict) and data.get("status_msg"):
                messages.append(str(data["status_msg"]))
        detail = "；".join(dict.fromkeys(messages))
        if "登录" in detail and not self.cookie:
            raise RuntimeError("抖音搜索要求登录，请到系统设置填写浏览器中的抖音 Cookie 后重试")
        raise RuntimeError(f"搜索接口未返回视频{('：' + detail) if detail else ''}")

    def video_detail(self, aweme_id: str):
        payload = {"aweme_id": aweme_id}
        if self.cookie:
            payload["cookie"] = self.cookie
        return self.post("/api/douyin/aweme_detail", payload)
