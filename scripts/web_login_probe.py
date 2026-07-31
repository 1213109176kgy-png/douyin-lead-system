from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from app.douyin_login import DouyinLoginDialog


app = QApplication([])
dialog = DouyinLoginDialog()
result = {"loaded": False, "url": "", "title": "", "cookies": 0}


def loaded(ok):
    result.update(loaded=bool(ok), url=dialog.web.url().toString(), title=dialog.web.title())
    dialog.store.loadAllCookies()
    QTimer.singleShot(1000, finish)


def finish():
    result["cookies"] = len(dialog.cookies)
    print(result)
    dialog.close()
    app.quit()


dialog.web.loadFinished.connect(loaded)
QTimer.singleShot(25000, finish)
dialog.show()
app.exec()
