from app.video_ai import choose_media_url, fill_prompt, find_media_url, safe_video_filename, shorten


def test_video_helpers():
    assert shorten("一二三四五", 3) == "一二三…"
    assert fill_prompt("{video_title}-{unknown}", video_title="工牌") == "工牌-{unknown}"
    payload = {"data": {"video": {"play_addr": {"url_list": ["https://video.test/a.mp4"]}}}}
    assert find_media_url(payload) == "https://video.test/a.mp4"


def test_choose_media_url_prefers_video_cdn_and_removes_duplicates():
    assert choose_media_url([
        "https://www.douyin.com/fallback.mp4",
        "https://v11-weba.douyinvod.com/real.mp4",
        "https://v11-weba.douyinvod.com/real.mp4",
    ]) == "https://v11-weba.douyinvod.com/real.mp4"


def test_safe_video_filename_removes_windows_invalid_characters():
    assert safe_video_filename('标题:测试/视频?*', '123') == '标题_测试_视频.mp4'
    assert safe_video_filename('', '123') == '123.mp4'
