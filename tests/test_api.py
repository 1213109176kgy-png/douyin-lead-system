import json
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
        rows = payload if isinstance(payload, list) else [payload]
        self.body = "\n".join(json.dumps(row) for row in rows).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def test_open_source_ndjson_comment_adapter():
    client = LocalApiClient(delay=0.8)
    row = {"id": "c1", "text": "多少钱", "author_id": "u1", "author_nick": "客户"}
    with patch("app.api_client.urllib.request.urlopen", return_value=_Response([row])) as urlopen, patch("app.api_client.time.sleep"):
        result = client.post("/api/douyin/video_comment", {"aweme_id": "1"})
    assert result == {"comments": [row], "has_more": False, "cursor": ""}
    assert "/v1/comments/1" in urlopen.call_args.args[0]


def test_flat_open_source_records_are_normalized():
    videos = parse_videos([{"id": "v2", "desc": "本地接口", "author_sec_uid": "a2", "author_nick": "作者", "digg_count": 9}])
    comments = parse_comments([{"id": "c2", "text": "怎么购买", "author_id": "u2", "author_nick": "客户2"}])
    assert videos[0]["author_name"] == "作者"
    assert videos[0]["digg_count"] == 9
    assert comments[0]["nickname"] == "客户2"


def test_comment_region_is_normalized():
    comments = parse_comments([{"id": "c3", "text": "想了解", "author_id": "u3", "author_nick": "客户3", "ip_label": "IP属地：北京"}])
    assert comments[0]["region"] == "北京"


def test_profile_url_requires_sec_uid_not_numeric_uid():
    numeric = parse_comments([{"id": "c4", "text": "咨询", "author_id": "123456", "author_nick": "客户"}])[0]
    secure = parse_comments([{"id": "c5", "text": "咨询", "author_id": "123456", "author_sec_uid": "MS4wLjABAAAAreal", "author_nick": "客户"}])[0]
    assert numeric["profile_url"] == ""
    assert secure["profile_url"] == "https://www.douyin.com/user/MS4wLjABAAAAreal"
