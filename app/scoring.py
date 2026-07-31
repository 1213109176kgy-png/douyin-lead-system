from __future__ import annotations

import re
from dataclasses import dataclass


DEFAULT_RULES = {
    "购买": (4, "想买|我要|怎么买|下单|订购|求购|需要|来一个|买一个"),
    "联系": (4, "联系|私信|微信|电话|加v|联系方式|怎么联系"),
    "价格": (3, "多少钱|价格|报价|怎么卖|怎么收费|费用|预算|多少一个"),
    "现货": (3, "有货|现货|能做吗|可以做吗|哪里买|哪有卖"),
    "采购": (3, "定制|批发|代理|加盟|合作|团购|采购|一批"),
    "位置": (2, "在哪里|地址|门店|哪个城市|本地有吗|哪里有"),
    "细节": (2, "型号|尺寸|材质|参数|怎么用|怎么做|介绍一下|支持什么"),
}
DEFAULT_NEGATIVES = "兼职刷单|刷单|免费领|日赚|招聘代理|互关互赞"
PHONE_RE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
WECHAT_RE = re.compile(r"(?i)(微信|vx|v信|加v)\s*[:：]?\s*([a-z][-_a-z0-9]{5,19})")


@dataclass(frozen=True)
class ScoreResult:
    score: int
    level: str
    matched: tuple[str, ...]
    excluded: bool = False


def normalize(text: object) -> str:
    return re.sub(r"\s+", "", str(text or "")).casefold()


def redact_pii(text: str) -> str:
    text = PHONE_RE.sub("[手机号已隐藏]", text)
    return WECHAT_RE.sub(lambda m: f"{m.group(1)} [微信号已隐藏]", text)


def score_comment(text: str, keywords: list[str], rules: dict | None = None, negatives: str = DEFAULT_NEGATIVES) -> ScoreResult:
    normalized = normalize(text)
    if any(normalize(term) in normalized for term in negatives.split("|") if term):
        return ScoreResult(-10, "排除", ("疑似垃圾推广",), True)
    active = rules or DEFAULT_RULES
    score, matched = 0, []
    for category, (weight, terms_text) in active.items():
        hits = [term for term in terms_text.split("|") if normalize(term) in normalized]
        if hits:
            score += int(weight)
            matched.extend(f"{category}:{term}" for term in hits[:2])
    if "?" in text or "？" in text:
        score += 1
        matched.append("问句")
    for keyword in keywords:
        if normalize(keyword) and normalize(keyword) in normalized:
            score += 2
            matched.append(f"关键词:{keyword}")
    level = "高" if score >= 7 else "中" if score >= 4 else "低" if score >= 2 else "排除"
    return ScoreResult(score, level, tuple(matched), level == "排除")
