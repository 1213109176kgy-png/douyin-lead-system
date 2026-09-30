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
from app.main_window import MainWindow
from app.paths import resolve_paths


shots = root / "data" / "screenshots"
shots.mkdir(parents=True, exist_ok=True)
app = QApplication([])
window = MainWindow(resolve_paths(root))
window.nav.setCurrentRow(7)
window.show()
app.processEvents()
window.grab().save(str(shots / "settings.png"))

def finish():
    window.close()
    app.quit()


QTimer.singleShot(7000, finish)
app.exec()
print(shots / "settings.png")
