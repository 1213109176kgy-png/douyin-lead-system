from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
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
        aweme_id = str(first(node, ("aweme_id", "item_id", "id"), ""))
        if not aweme_id or aweme_id in seen: continue
        author = node.get("author") if isinstance(node.get("author"), dict) else {}
        statistics = node.get("statistics") if isinstance(node.get("statistics"), dict) else {}
        found.append({"aweme_id": aweme_id, "title": str(first(node, ("desc", "title", "caption"), "")), "url": str(first(node, ("share_url", "url"), f"https://www.douyin.com/video/{aweme_id}")), "author_uid": str(first(author, ("sec_uid", "sec_user_id", "uid"), first(node, ("author_sec_uid",), ""))), "author_name": str(first(author, ("nickname", "name"), first(node, ("author_nick", "author"), ""))), "digg_count": int(first(statistics, ("digg_count", "like_count"), first(node, ("digg_count",), 0)) or 0), "collect_count": int(first(statistics, ("collect_count", "favorite_count"), first(node, ("collect_count",), 0)) or 0), "comment_count": int(first(statistics, ("comment_count",), first(node, ("comment_count",), 0)) or 0)})
        seen.add(aweme_id)
    return found


def parse_comments(payload) -> list[dict]:
    found, seen = [], set()
    for node in walk(payload):
        text = first(node, ("text", "comment_text", "content"), "")
        user = first(node, ("user", "comment_user"), {})
        if not user and isinstance(node.get("author"), dict):
            user = node["author"]
        if not isinstance(text, str) or not text.strip() or not isinstance(user, dict): continue
        cid = str(first(node, ("cid", "comment_id", "id"), ""))
        sec_uid = str(first(user, ("sec_uid", "sec_user_id"), first(node, ("author_sec_uid",), "")))
        numeric_uid = str(first(user, ("uid", "user_id"), first(node, ("author_id",), "")))
        uid = sec_uid or numeric_uid
        nickname = str(first(user, ("nickname", "name", "display_name"), first(node, ("author_nick", "author"), "")))
        key = cid or f"{uid}:{text.strip()}"
        if key in seen or not (uid or nickname): continue
        region = str(first(node, ("region", "ip_label", "ip_location"), "")).replace("IP属地：", "").strip()
        profile_url = str(first(user, ("share_url", "profile_url"), ""))
        if not profile_url and sec_uid:
            profile_url = f"https://www.douyin.com/user/{sec_uid}"
        found.append({"comment_id": cid, "text": text.strip(), "user_id": uid, "nickname": nickname, "region": region, "likes": int(first(node, ("digg_count", "like_count"), 0) or 0), "created_at": str(first(node, ("create_time", "timestamp"), "")), "profile_url": profile_url})
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
        if endpoint == "/api/douyin/video_comment":
            rows = self.get_rows(f"/v1/comments/{urllib.parse.quote(str(payload['aweme_id']), safe='')}", {"limit": payload.get("count", 50)}, retries)
            return {"comments": rows, "has_more": False, "cursor": ""}
        if endpoint == "/api/douyin/aweme_detail":
            rows = self.get_rows(f"/v1/video/{urllib.parse.quote(str(payload['aweme_id']), safe='')}", {}, retries)
            return rows[0] if rows else {}
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

    def get_rows(self, endpoint: str, params: dict | None = None, retries=3) -> list[dict]:
        query = urllib.parse.urlencode(params or {})
        url = self.base_url + endpoint + (("?" + query) if query else "")
        for attempt in range(retries):
            wait = self.delay - (time.monotonic() - self.last_request)
            if wait > 0: time.sleep(wait)
            self.last_request = time.monotonic()
            try:
                with urllib.request.urlopen(url, timeout=45) as response:
                    text = response.read().decode("utf-8").strip()
                return [json.loads(line) for line in text.splitlines() if line.strip()]
            except urllib.error.HTTPError as exc:
                if attempt >= retries - 1:
                    raise RuntimeError(f"本地接口错误 HTTP {exc.code}") from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt >= retries - 1:
                    raise RuntimeError(f"本地接口请求失败：{exc}") from exc
            time.sleep(min(2 ** attempt, 4))
        return []

    def search_videos(self, keyword: str, count: int):
        path = "/v1/search/" + urllib.parse.quote(keyword, safe="")
        hits = self.get_rows(path, {"limit": min(count, 100)})
        videos = []
        for hit in hits:
            if hit.get("type") not in ("video", "aweme", ""):
                continue
            aweme_id = str(hit.get("id", ""))
            if not aweme_id:
                continue
            detail = self.video_detail(aweme_id)
            videos.extend(parse_videos(detail))
            if len(videos) >= count:
                break
        if videos:
            return hits, videos
        if not self.cookie:
            raise RuntimeError("尚未登录抖音，请先在系统设置中完成登录")
        raise RuntimeError("抖音接口返回空结果。这不是未登录，而是独立接口受到平台风控；请使用已登录浏览器搜索")

    def video_detail(self, aweme_id: str):
        return self.post("/api/douyin/aweme_detail", {"aweme_id": aweme_id})
