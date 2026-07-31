from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    root: Path
    data: Path
    logs: Path
    exports: Path
    backups: Path
    server: Path
    database: Path
    settings: Path

    def ensure(self) -> "AppPaths":
        for directory in (self.data, self.logs, self.exports, self.backups):
            directory.mkdir(parents=True, exist_ok=True)
        return self


def resolve_paths(root_override: str | Path | None = None) -> AppPaths:
    if root_override:
        root = Path(root_override).resolve()
    elif getattr(sys, "frozen", False):
        root = Path(sys.executable).resolve().parent
    else:
        root = Path(__file__).resolve().parents[1]
    data = Path(os.environ.get("DOUYIN_LEAD_DATA_DIR", root / "data")).resolve()
    return AppPaths(
        root=root,
        data=data,
        logs=data / "logs",
        exports=data / "exports",
        backups=data / "backups",
        server=root / "server" / "APIServer_v5.3.1",
        database=data / "leads.db",
        settings=data / "settings.json",
    )
