from datetime import datetime, timedelta

from app.collector import comment_matches_filters


def test_region_filter_accepts_one_of_multiple_regions():
    comment = {"region": "北京", "created_at": ""}
    assert comment_matches_filters(comment, "上海,北京", "不限")
    assert not comment_matches_filters(comment, "广东", "不限")


def test_time_filters_use_comment_timestamp():
    now = datetime(2026, 9, 29, 12, 0, 0)
    recent = {"region": "", "created_at": str(int((now - timedelta(days=2)).timestamp()))}
    old = {"region": "", "created_at": str(int((now - timedelta(days=8)).timestamp()))}
    assert comment_matches_filters(recent, "", "近3天", now)
    assert not comment_matches_filters(old, "", "近7天", now)
