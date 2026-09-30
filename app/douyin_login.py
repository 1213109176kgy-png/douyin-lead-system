from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from .douyin_browser import EdgeLoginWorker


AUTH_COOKIE_NAMES = {"sessionid", "sessionid_ss", "sid_guard"}


def cookie_header(cookies: dict[str, str]) -> str:
    return "; ".join(f"{name}={value}" for name, value in sorted(cookies.items()) if name and value)


def has_login_cookie(cookies: dict[str, str]) -> bool:
    if any(cookies.get(name) for name in AUTH_COOKIE_NAMES):
        return True
    return cookies.get("passport_auth_status", "").lower() in {"1", "true", "success"}


class DouyinLoginDialog(QDialog):
    def __init__(self, data_dir: Path, parent=None):
        super().__init__(parent)
        self.data_dir = Path(data_dir)
        self.setWindowTitle("登录抖音")
        self.resize(560, 230)
        self.setMinimumSize(520, 210)
        self.cookie_value = ""
        self.status = QLabel(
            "正在打开独立浏览器窗口。优先使用 Microsoft Edge；没有 Edge 时会自动使用软件内置浏览器。\n\n"
            "请只在该窗口登录抖音；程序不会读取你的个人浏览器资料。"
        )
        self.status.setWordWrap(True)
        self.open_button = QPushButton("重新打开登录窗口")
        cancel = QPushButton("取消")
        self.open_button.clicked.connect(self._start_worker)
        cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addStretch(); buttons.addWidget(self.open_button); buttons.addWidget(cancel)
        layout = QVBoxLayout(self)
        layout.addWidget(self.status, 1); layout.addLayout(buttons)
        self.worker: EdgeLoginWorker | None = None
        self._start_worker()

    def _start_worker(self):
        if self.worker and self.worker.isRunning(): return
        self.open_button.setEnabled(False)
        self.worker = EdgeLoginWorker(self.data_dir, self)
        self.worker.status.connect(self.status.setText)
        self.worker.logged_in.connect(self._logged_in)
        self.worker.failed.connect(self._failed)
        self.worker.finished.connect(lambda: self.open_button.setEnabled(True))
        self.worker.start()

    def _logged_in(self, header: str):
        self.cookie_value = header
        self.status.setText("已检测到登录状态，正在保存…")
        self.accept()

    def _failed(self, message: str):
        self.status.setText(message)
        self.open_button.setEnabled(True)

    def reject(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel(); self.worker.wait(5000)
        super().reject()
