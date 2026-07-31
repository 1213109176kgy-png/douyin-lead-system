from __future__ import annotations

import shutil
import tempfile
import urllib.request
from pathlib import Path

from .ai_client import DEFAULT_ANALYSIS_PROMPT, DEFAULT_REWRITE_PROMPT, OpenAICompatibleClient


def shorten(text: str, length: int = 30) -> str:
    text = str(text or "")
    return text if len(text) <= length else text[:length] + "…"


def fill_prompt(template: str, **values) -> str:
    class Safe(dict):
        def __missing__(self, key):
            return "{" + key + "}"
    return template.format_map(Safe({key: str(value or "") for key, value in values.items()}))


def find_media_url(payload) -> str:
    def walk(value):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
    for node in walk(payload):
        for key in ("play_addr", "download_addr", "play_url"):
            address = node.get(key)
            if isinstance(address, dict):
                urls = address.get("url_list") or address.get("urlList") or []
                if urls:
                    return str(urls[0])
            if isinstance(address, str) and address.startswith("http"):
                return address
    return ""


def download_media(url: str, target: Path, cookie: str = "") -> Path:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    if cookie:
        headers["Cookie"] = cookie
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)
    return target


def transcribe_local(media_path: Path, model_dir: Path, progress=lambda _text: None) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("本地 Whisper 组件未安装，请使用完整版绿色包") from exc
    model_dir.mkdir(parents=True, exist_ok=True)
    progress("正在加载或首次下载 Whisper base 模型…")
    model = WhisperModel("base", device="cpu", compute_type="int8", download_root=str(model_dir))
    progress("正在识别视频口播…")
    segments, _info = model.transcribe(str(media_path), language="zh", vad_filter=True, beam_size=5)
    return "\n".join(segment.text.strip() for segment in segments if segment.text.strip())


def analyze_video(client: OpenAICompatibleClient, template: str, video, transcript: str) -> str:
    return client.chat(fill_prompt(template or DEFAULT_ANALYSIS_PROMPT, industry_keyword=video["keyword"], video_title=video["title"], video_author=video["author_name"], transcript=transcript))


def rewrite_video(client: OpenAICompatibleClient, template: str, video, requirements: str) -> str:
    return client.chat(fill_prompt(template or DEFAULT_REWRITE_PROMPT, industry_keyword=video["keyword"], video_title=video["title"], analysis_result=video["analysis"], rewrite_requirements=requirements))

