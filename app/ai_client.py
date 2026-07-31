from __future__ import annotations

import json
import urllib.error
import urllib.request


DEFAULT_ANALYSIS_PROMPT = """你是一名短视频营销拆解专家。请根据以下信息拆解视频。
行业关键词：{industry_keyword}
视频标题：{video_title}
作者：{video_author}
口播原文：
{transcript}

请严格输出：1.完整口播稿校订版；2.开头钩子；3.目标人群与痛点；4.核心卖点；
5.内容结构；6.情绪与表达方式；7.信任背书；8.转化动作；9.可复用句式；10.仿写建议。"""

DEFAULT_REWRITE_PROMPT = """你是一名短视频爆款口播编剧。请基于拆解结果进行原创仿写，不得逐句抄袭。
行业关键词：{industry_keyword}
原视频标题：{video_title}
拆解结果：
{analysis_result}
本次要求：{rewrite_requirements}

输出：新标题、完整口播稿、分镜/字幕建议、结尾转化话术。"""


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 90, temperature: float = 0.7):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.temperature = temperature

    def chat(self, prompt: str) -> str:
        if not self.base_url or not self.api_key or not self.model:
            raise RuntimeError("请先在系统设置中配置 AI API 地址、API Key 和模型名称")
        endpoint = self.base_url if self.base_url.endswith("/chat/completions") else self.base_url + "/chat/completions"
        body = json.dumps({"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": self.temperature}, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(endpoint, data=body, method="POST", headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"AI 接口调用失败：{exc}") from exc

