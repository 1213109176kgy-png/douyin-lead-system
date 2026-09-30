from __future__ import annotations

import base64
import ctypes
import json
import os
from ctypes import wintypes
from pathlib import Path


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob(data: bytes):
    buffer = ctypes.create_string_buffer(data)
    return DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer


def protect(value: str) -> str:
    raw = value.encode("utf-8")
    if os.name != "nt":
        return "plain-test:" + base64.b64encode(raw).decode("ascii")
    source, keepalive = _blob(raw)
    target = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(source), "DouyinLead", None, None, None, 0, ctypes.byref(target)):
        raise ctypes.WinError()
    try:
        encrypted = ctypes.string_at(target.pbData, target.cbData)
        return "dpapi:" + base64.b64encode(encrypted).decode("ascii")
    finally:
        ctypes.windll.kernel32.LocalFree(target.pbData)


def unprotect(value: str) -> str:
    prefix, encoded = value.split(":", 1)
    raw = base64.b64decode(encoded)
    if prefix == "plain-test" and os.name != "nt":
        return raw.decode("utf-8")
    if prefix != "dpapi" or os.name != "nt":
        raise ValueError("unsupported secret format")
    source, keepalive = _blob(raw)
    target = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 0, ctypes.byref(target)):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(target.pbData, target.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(target.pbData)


class SettingsStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, values: dict):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")

    def set_secret(self, key: str, value: str):
        data = self.load(); data[key] = protect(value) if value else ""; self.save(data)

    def get_secret(self, key: str) -> str:
        value = self.load().get(key, "")
        return unprotect(value) if value else ""

    def clear_secret(self, key: str):
        data = self.load()
        data.pop(key, None)
        self.save(data)

    def update(self, **values):
        data = self.load(); data.update(values); self.save(data)


def save_ai_configuration(
    store: SettingsStore,
    api_key: str,
    base_url: str,
    model: str,
    temperature: float,
    analysis_prompt: str,
    rewrite_prompt: str,
):
    """Persist the exact AI configuration used by connection tests and workers."""
    if api_key:
        store.set_secret("ai_api_key", api_key)
    store.update(
        ai_base_url=base_url.strip(),
        ai_model=model.strip(),
        ai_temperature=float(temperature),
        ai_timeout=90,
        analysis_prompt=analysis_prompt,
        rewrite_prompt=rewrite_prompt,
    )
