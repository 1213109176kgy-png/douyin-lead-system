from __future__ import annotations

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


AUTH_COOKIE_NAMES = {
    "sessionid",
    "sessionid_ss",
    "sid_guard",
}


def cookie_header(cookies: dict[str, str]) -> str:
    return "; ".join(f"{name}={value}" for name, value in sorted(cookies.items()) if name and value)


def has_login_cookie(cookies: dict[str, str]) -> bool:
    if any(cookies.get(name) for name in AUTH_COOKIE_NAMES):
        return True
    return cookies.get("passport_auth_status", "").lower() in {"1", "true", "success"}


class DouyinLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("登录抖音")
        self.resize(1040, 760)
        self.setMinimumSize(820, 620)
        self.cookie_value = ""
        self.cookies: dict[str, str] = {}
        self._accept_timer = QTimer(self)
        self._accept_timer.setSingleShot(True)
        self._accept_timer.timeout.connect(self._save_and_accept)

        # Unnamed profiles are off-the-record. Web cookies stay in memory and
        # only the resulting Cookie header is persisted using Windows DPAPI.
        self.profile = QWebEngineProfile(self)
        self.store = self.profile.cookieStore()
        self.store.cookieAdded.connect(self._on_cookie_added)
        self.store.cookieRemoved.connect(self._on_cookie_removed)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
        self.web = QWebEngineView(self)
        self.page = QWebEnginePage(self.profile, self.web)
        self.web.setPage(self.page)
        self.web.loadFinished.connect(lambda _ok: self.store.loadAllCookies())
        self.web.setUrl(QUrl("https://www.douyin.com/"))

        self.status = QLabel("请在下方扫码或登录抖音。检测到登录成功后会自动保存并关闭。")
        self.status.setWordWrap(True)
        done = QPushButton("我已登录，保存")
        cancel = QPushButton("取消")
        done.clicked.connect(self._manual_save)
        cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(done)
        buttons.addWidget(cancel)
        layout = QVBoxLayout(self)
        layout.addWidget(self.status)
        layout.addWidget(self.web, 1)
        layout.addLayout(buttons)

    def _on_cookie_added(self, cookie):
        if "douyin.com" not in cookie.domain().lower():
            return
        name = bytes(cookie.name()).decode("utf-8", errors="ignore")
        value = bytes(cookie.value()).decode("utf-8", errors="ignore")
        if name and value:
            self.cookies[name] = value
        if has_login_cookie(self.cookies):
            self.status.setText("已检测到抖音登录状态，正在安全保存…")
            self._accept_timer.start(1500)

    def _on_cookie_removed(self, cookie):
        name = bytes(cookie.name()).decode("utf-8", errors="ignore")
        self.cookies.pop(name, None)

    def _manual_save(self):
        self.store.loadAllCookies()
        if not has_login_cookie(self.cookies):
            self.status.setText("暂未检测到登录状态，请先完成扫码或账号登录。")
            return
        self._save_and_accept()

    def _save_and_accept(self):
        if has_login_cookie(self.cookies):
            self.cookie_value = cookie_header(self.cookies)
            self.accept()
