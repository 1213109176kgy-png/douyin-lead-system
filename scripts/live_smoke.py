from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


root = Path(__file__).resolve().parents[1]
server_root = root / "server" / "APIServer_v5.3.1"
log_path = root / "data" / "logs" / "apiserver-live-test.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env["PYTHONPATH"] = str(root)
with log_path.open("w", encoding="utf-8") as log:
    process = subprocess.Popen(
        [sys.executable, "-m", "app.main", "--server", str(server_root)],
        cwd=server_root,
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    try:
        ready = False
        for _ in range(60):
            time.sleep(0.5)
            try:
                with socket.create_connection(("127.0.0.1", 8001), timeout=0.5):
                    ready = True
                    break
            except OSError:
                pass
        print(json.dumps({"ready": ready, "pid": process.pid}, ensure_ascii=False))
        if ready:
            for endpoint in ("search_video", "search_video_v2", "search_video_v3"):
                payload = json.dumps({"keyword": "销售工牌", "count": "3", "offset": "0"}, ensure_ascii=False).encode("utf-8")
                request = urllib.request.Request(
                    f"http://127.0.0.1:8001/api/douyin/{endpoint}",
                    data=payload,
                    method="POST",
                    headers={"Content-Type": "application/json;charset=utf-8"},
                )
                try:
                    with urllib.request.urlopen(request, timeout=90) as response:
                        result = json.loads(response.read().decode("utf-8"))
                    print(endpoint, json.dumps(result, ensure_ascii=False)[:3000])
                except Exception as exc:
                    print(endpoint, type(exc).__name__, str(exc))
    finally:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
