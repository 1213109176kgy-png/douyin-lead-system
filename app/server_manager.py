from __future__ import annotations

import os
import socket
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


class ServerManager:
    def __init__(self, server_root: Path, log_path: Path, port: int = 8001):
        self.server_root = Path(server_root)
        self.log_path = Path(log_path)
        self.port = port
        self.process: subprocess.Popen | None = None
        self._log_handle = None

    @property
    def base_url(self):
        return f"http://127.0.0.1:{self.port}"

    def is_ready(self) -> bool:
        try:
            with socket.create_connection(("127.0.0.1", self.port), timeout=1):
                return True
        except OSError:
            return False

    def local_binary(self) -> Path:
        return self.server_root.parent / "douyin-local.exe"

    def build_command(self) -> list[str]:
        return [str(self.local_binary()), "serve", "--addr", f"127.0.0.1:{self.port}"]

    @staticmethod
    def prepare_ca_bundle() -> Path:
        import certifi

        source = Path(certifi.where())
        public = Path(os.environ.get("PUBLIC", r"C:\Users\Public"))
        candidates = (
            public / "DouyinLeadSystem" / "cacert.pem",
            Path(tempfile.gettempdir()) / "DouyinLeadSystem" / "cacert.pem",
        )
        last_error = None
        for target in candidates:
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or target.stat().st_size != source.stat().st_size:
                    shutil.copy2(source, target)
                return target
            except OSError as exc:
                last_error = exc
        raise RuntimeError(f"无法准备 HTTPS 证书文件：{last_error}")

    def start(self, cookie: str = "", timeout: float = 35) -> tuple[bool, str]:
        if self.is_ready():
            return True, "本地服务已运行"
        binary = self.local_binary()
        if not binary.exists():
            return False, f"未找到开源本地服务：{binary}"
        env = os.environ.copy()
        if cookie.strip():
            env["DOUYIN_COOKIE"] = cookie.strip()
        env["PYTHONUTF8"] = "1"
        project_root = str(Path(__file__).resolve().parents[1])
        env["PYTHONPATH"] = project_root + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_handle = self.log_path.open("a", encoding="utf-8")
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        self.process = subprocess.Popen(self.build_command(), cwd=binary.parent, env=env, stdout=self._log_handle, stderr=subprocess.STDOUT, creationflags=flags)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                return False, f"本地服务启动失败，退出码 {self.process.returncode}，请查看日志"
            if self.is_ready():
                return True, "本地服务启动成功"
            time.sleep(0.5)
        return False, "本地服务启动超时，请检查日志"

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None
        if self._log_handle:
            self._log_handle.close(); self._log_handle = None
