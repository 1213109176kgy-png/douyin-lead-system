import io
import json
import urllib.error
from unittest.mock import patch

from app.api_client import LocalApiClient, parse_comments, parse_videos


def test_schema_tolerant_parsing():
    videos = parse_videos({"data": [{"aweme_id": "v1", "desc": "销售工牌", "author": {"sec_uid": "a1"}, "statistics": {"digg_count": 10, "collect_count": 3, "comment_count": 8}}]})
    comments = parse_comments({"comments": [{"cid": "c1", "text": "多少钱", "user": {"sec_uid": "u1", "nickname": "客户"}}]})
    assert videos[0]["aweme_id"] == "v1"
    assert (videos[0]["digg_count"], videos[0]["collect_count"], videos[0]["comment_count"]) == (10, 3, 8)
    assert comments[0]["nickname"] == "客户"


class _Response:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def test_startup_401_is_retried_until_moreapi_is_ready():
    unauthorized = urllib.error.HTTPError(
        "http://127.0.0.1:8001/api/douyin/video_comment",
        401,
        "MoreAPI未准备完毕",
        {},
        io.BytesIO(b""),
    )
    client = LocalApiClient(delay=0.8)

    with patch(
        "app.api_client.urllib.request.urlopen",
        side_effect=[unauthorized, unauthorized, unauthorized, _Response({"comments": []})],
    ) as urlopen, patch("app.api_client.time.sleep") as sleep:
        result = client.post("/api/douyin/video_comment", {"aweme_id": "1"})

    assert result == {"comments": []}
    assert urlopen.call_count == 4
    assert sleep.call_count >= 3


def test_persistent_startup_401_still_reports_actionable_error():
    unauthorized = urllib.error.HTTPError(
        "http://127.0.0.1:8001/api/douyin/video_comment",
        401,
        "Unauthorized",
        {},
        io.BytesIO(b""),
    )
    client = LocalApiClient(delay=0.8)

    with patch("app.api_client.urllib.request.urlopen", side_effect=unauthorized), patch(
        "app.api_client.time.sleep"
    ):
        try:
            client.post("/api/douyin/video_comment", {"aweme_id": "1"})
        except RuntimeError as exc:
            assert "初始化超时" in str(exc)
        else:
            raise AssertionError("persistent HTTP 401 should fail after bounded retries")
