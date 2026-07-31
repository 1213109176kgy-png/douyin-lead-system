from __future__ import annotations

import sys


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--server":
        from .server_bootstrap import run_server
        run_server(sys.argv[2]); return 0
    from PySide6.QtWidgets import QApplication
    from .main_window import MainWindow
    from .paths import resolve_paths
    from .theme import APP_STYLE
    app=QApplication(sys.argv); app.setApplicationName("抖音获客系统"); app.setStyleSheet(APP_STYLE)
    window=MainWindow(resolve_paths()); window.show(); return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
