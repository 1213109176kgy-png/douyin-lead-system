from app.video_ai import fill_prompt, find_media_url, shorten


def test_video_helpers():
    assert shorten("一二三四五", 3) == "一二三…"
    assert fill_prompt("{video_title}-{unknown}", video_title="工牌") == "工牌-{unknown}"
    payload = {"data": {"video": {"play_addr": {"url_list": ["https://video.test/a.mp4"]}}}}
    assert find_media_url(payload) == "https://video.test/a.mp4"
