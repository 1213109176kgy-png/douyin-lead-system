from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    pythonw = root / "runtime" / "pythonw.exe"
    if not pythonw.exists():
        raise SystemExit("绿色版运行环境不完整：缺少 runtime/pythonw.exe")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    env["PYTHONUTF8"] = "1"
    subprocess.Popen(
        [str(pythonw), "-m", "app.main"],
        cwd=root,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
