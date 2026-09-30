import sys
from types import SimpleNamespace

import pytest

from app.video_ai import choose_media_url, fill_prompt, find_media_url, safe_video_filename, shorten, transcribe_local


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


def test_transcribe_without_audio_returns_empty(monkeypatch, tmp_path):
    class FakeModel:
        def __init__(self, *_args, **_kwargs):
            pass

        def transcribe(self, *_args, **_kwargs):
            raise IndexError("tuple index out of range")

    monkeypatch.setitem(sys.modules, "faster_whisper", SimpleNamespace(WhisperModel=FakeModel))
    messages = []

    result = transcribe_local(tmp_path / "silent.mp4", tmp_path / "models", messages.append)

    assert result == ""
    assert messages[-1] == "视频没有可识别的音轨，将跳过口播识别…"


def test_transcribe_does_not_hide_unrelated_index_error(monkeypatch, tmp_path):
    class FakeModel:
        def __init__(self, *_args, **_kwargs):
            pass

        def transcribe(self, *_args, **_kwargs):
            raise IndexError("unexpected model failure")

    monkeypatch.setitem(sys.modules, "faster_whisper", SimpleNamespace(WhisperModel=FakeModel))

    with pytest.raises(IndexError, match="unexpected model failure"):
        transcribe_local(tmp_path / "broken.mp4", tmp_path / "models")
